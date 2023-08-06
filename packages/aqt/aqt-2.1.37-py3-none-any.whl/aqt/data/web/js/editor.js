"use strict";
/* Copyright: Ankitects Pty Ltd and contributors
 * License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html */
let currentField = null;
let changeTimer = null;
let currentNoteId = null;
/* kept for compatibility with add-ons */
String.prototype.format = function () {
    const args = arguments;
    return this.replace(/\{\d+\}/g, function (m) {
        return args[m.match(/\d+/)];
    });
};
function setFGButton(col) {
    $("#forecolor")[0].style.backgroundColor = col;
}
function saveNow(keepFocus) {
    if (!currentField) {
        return;
    }
    clearChangeTimer();
    if (keepFocus) {
        saveField("key");
    }
    else {
        // triggers onBlur, which saves
        currentField.blur();
    }
}
function triggerKeyTimer() {
    clearChangeTimer();
    changeTimer = setTimeout(function () {
        updateButtonState();
        saveField("key");
    }, 600);
}
function onKey(evt) {
    // esc clears focus, allowing dialog to close
    if (evt.which === 27) {
        currentField.blur();
        return;
    }
    // shift+tab goes to previous field
    if (navigator.platform === "MacIntel" && evt.which === 9 && evt.shiftKey) {
        evt.preventDefault();
        focusPrevious();
        return;
    }
    // fix Ctrl+right/left handling in RTL fields
    if (currentField.dir === "rtl") {
        const selection = window.getSelection();
        let granularity = "character";
        let alter = "move";
        if (evt.ctrlKey) {
            granularity = "word";
        }
        if (evt.shiftKey) {
            alter = "extend";
        }
        if (evt.which === 39) {
            selection.modify(alter, "right", granularity);
            evt.preventDefault();
            return;
        }
        else if (evt.which === 37) {
            selection.modify(alter, "left", granularity);
            evt.preventDefault();
            return;
        }
    }
    triggerKeyTimer();
}
function insertNewline() {
    if (!inPreEnvironment()) {
        setFormat("insertText", "\n");
        return;
    }
    // in some cases inserting a newline will not show any changes,
    // as a trailing newline at the end of a block does not render
    // differently. so in such cases we note the height has not
    // changed and insert an extra newline.
    const r = window.getSelection().getRangeAt(0);
    if (!r.collapsed) {
        // delete any currently selected text first, making
        // sure the delete is undoable
        setFormat("delete");
    }
    const oldHeight = currentField.clientHeight;
    setFormat("inserthtml", "\n");
    if (currentField.clientHeight === oldHeight) {
        setFormat("inserthtml", "\n");
    }
}
// is the cursor in an environment that respects whitespace?
function inPreEnvironment() {
    let n = window.getSelection().anchorNode;
    if (n.nodeType === 3) {
        n = n.parentNode;
    }
    return window.getComputedStyle(n).whiteSpace.startsWith("pre");
}
function onInput() {
    // empty field?
    if (currentField.innerHTML === "") {
        currentField.innerHTML = "<br>";
    }
    // make sure IME changes get saved
    triggerKeyTimer();
}
function updateButtonState() {
    const buts = ["bold", "italic", "underline", "superscript", "subscript"];
    for (const name of buts) {
        if (document.queryCommandState(name)) {
            $("#" + name).addClass("highlighted");
        }
        else {
            $("#" + name).removeClass("highlighted");
        }
    }
    // fixme: forecolor
    //    'col': document.queryCommandValue("forecolor")
}
function toggleEditorButton(buttonid) {
    if ($(buttonid).hasClass("highlighted")) {
        $(buttonid).removeClass("highlighted");
    }
    else {
        $(buttonid).addClass("highlighted");
    }
}
function setFormat(cmd, arg, nosave = false) {
    document.execCommand(cmd, false, arg);
    if (!nosave) {
        saveField("key");
        updateButtonState();
    }
}
function clearChangeTimer() {
    if (changeTimer) {
        clearTimeout(changeTimer);
        changeTimer = null;
    }
}
function onFocus(elem) {
    if (currentField === elem) {
        // anki window refocused; current element unchanged
        return;
    }
    currentField = elem;
    pycmd("focus:" + currentFieldOrdinal());
    enableButtons();
    // don't adjust cursor on mouse clicks
    if (mouseDown) {
        return;
    }
    // do this twice so that there's no flicker on newer versions
    caretToEnd();
    // scroll if bottom of element off the screen
    function pos(obj) {
        let cur = 0;
        do {
            cur += obj.offsetTop;
        } while ((obj = obj.offsetParent));
        return cur;
    }
    const y = pos(elem);
    if (window.pageYOffset + window.innerHeight < y + elem.offsetHeight ||
        window.pageYOffset > y) {
        window.scroll(0, y + elem.offsetHeight - window.innerHeight);
    }
}
function focusField(n) {
    if (n === null) {
        return;
    }
    $("#f" + n).focus();
}
function focusPrevious() {
    if (!currentField) {
        return;
    }
    const previous = currentFieldOrdinal() - 1;
    if (previous >= 0) {
        focusField(previous);
    }
}
function focusIfField(x, y) {
    const elements = document.elementsFromPoint(x, y);
    for (let i = 0; i < elements.length; i++) {
        let elem = elements[i];
        if (elem.classList.contains("field")) {
            elem.focus();
            // the focus event may not fire if the window is not active, so make sure
            // the current field is set
            currentField = elem;
            return true;
        }
    }
    return false;
}
function onPaste(elem) {
    pycmd("paste");
    window.event.preventDefault();
}
function caretToEnd() {
    const r = document.createRange();
    r.selectNodeContents(currentField);
    r.collapse(false);
    const s = document.getSelection();
    s.removeAllRanges();
    s.addRange(r);
}
function onBlur() {
    if (!currentField) {
        return;
    }
    if (document.activeElement === currentField) {
        // other widget or window focused; current field unchanged
        saveField("key");
    }
    else {
        saveField("blur");
        currentField = null;
        disableButtons();
    }
}
function saveField(type) {
    clearChangeTimer();
    if (!currentField) {
        // no field has been focused yet
        return;
    }
    // type is either 'blur' or 'key'
    pycmd(type +
        ":" +
        currentFieldOrdinal() +
        ":" +
        currentNoteId +
        ":" +
        currentField.innerHTML);
}
function currentFieldOrdinal() {
    return currentField.id.substring(1);
}
function wrappedExceptForWhitespace(text, front, back) {
    const match = text.match(/^(\s*)([^]*?)(\s*)$/);
    return match[1] + front + match[2] + back + match[3];
}
function disableButtons() {
    $("button.linkb:not(.perm)").prop("disabled", true);
}
function enableButtons() {
    $("button.linkb").prop("disabled", false);
}
// disable the buttons if a field is not currently focused
function maybeDisableButtons() {
    if (!document.activeElement || document.activeElement.className !== "field") {
        disableButtons();
    }
    else {
        enableButtons();
    }
}
function wrap(front, back) {
    wrapInternal(front, back, false);
}
/* currently unused */
function wrapIntoText(front, back) {
    wrapInternal(front, back, true);
}
function wrapInternal(front, back, plainText) {
    const s = window.getSelection();
    let r = s.getRangeAt(0);
    const content = r.cloneContents();
    const span = document.createElement("span");
    span.appendChild(content);
    if (plainText) {
        const new_ = wrappedExceptForWhitespace(span.innerText, front, back);
        setFormat("inserttext", new_);
    }
    else {
        const new_ = wrappedExceptForWhitespace(span.innerHTML, front, back);
        setFormat("inserthtml", new_);
    }
    if (!span.innerHTML) {
        // run with an empty selection; move cursor back past postfix
        r = s.getRangeAt(0);
        r.setStart(r.startContainer, r.startOffset - back.length);
        r.collapse(true);
        s.removeAllRanges();
        s.addRange(r);
    }
}
function onCutOrCopy() {
    pycmd("cutOrCopy");
    return true;
}
function setFields(fields) {
    let txt = "";
    for (let i = 0; i < fields.length; i++) {
        const n = fields[i][0];
        let f = fields[i][1];
        if (!f) {
            f = "<br>";
        }
        txt += `
        <tr>
            <td class=fname id="name${i}">${n}</td>
        </tr>
        <tr>
            <td width=100%>
                <div id=f${i}
                     onkeydown='onKey(window.event);'
                     oninput='onInput();'
                     onmouseup='onKey(window.event);'
                     onfocus='onFocus(this);'
                     onblur='onBlur();'
                     class='field clearfix'
                     onpaste='onPaste(this);'
                     oncopy='onCutOrCopy(this);'
                     oncut='onCutOrCopy(this);'
                     contentEditable=true
                     class=field
                >${f}</div>
            </td>
        </tr>`;
    }
    $("#fields").html(`
    <table cellpadding=0 width=100% style='table-layout: fixed;'>
${txt}
    </table>`);
    maybeDisableButtons();
}
function setBackgrounds(cols) {
    for (let i = 0; i < cols.length; i++) {
        if (cols[i] == "dupe") {
            $("#f" + i).addClass("dupe");
        }
        else {
            $("#f" + i).removeClass("dupe");
        }
    }
}
function setFonts(fonts) {
    for (let i = 0; i < fonts.length; i++) {
        const n = $("#f" + i);
        n.css("font-family", fonts[i][0]).css("font-size", fonts[i][1]);
        n[0].dir = fonts[i][2] ? "rtl" : "ltr";
    }
}
function setNoteId(id) {
    currentNoteId = id;
}
function showDupes() {
    $("#dupes").show();
}
function hideDupes() {
    $("#dupes").hide();
}
/// If the field has only an empty br, remove it first.
let insertHtmlRemovingInitialBR = function (html) {
    if (html !== "") {
        // remove <br> in empty field
        if (currentField && currentField.innerHTML === "<br>") {
            currentField.innerHTML = "";
        }
        setFormat("inserthtml", html);
    }
};
let pasteHTML = function (html, internal, extendedMode) {
    html = filterHTML(html, internal, extendedMode);
    insertHtmlRemovingInitialBR(html);
};
let filterHTML = function (html, internal, extendedMode) {
    // wrap it in <top> as we aren't allowed to change top level elements
    const top = $.parseHTML("<ankitop>" + html + "</ankitop>")[0];
    if (internal) {
        filterInternalNode(top);
    }
    else {
        filterNode(top, extendedMode);
    }
    let outHtml = top.innerHTML;
    if (!extendedMode && !internal) {
        // collapse whitespace
        outHtml = outHtml.replace(/[\n\t ]+/g, " ");
    }
    outHtml = outHtml.trim();
    //console.log(`input html: ${html}`);
    //console.log(`outpt html: ${outHtml}`);
    return outHtml;
};
let allowedTagsBasic = {};
let allowedTagsExtended = {};
let TAGS_WITHOUT_ATTRS = ["P", "DIV", "BR", "SUB", "SUP"];
for (const tag of TAGS_WITHOUT_ATTRS) {
    allowedTagsBasic[tag] = { attrs: [] };
}
TAGS_WITHOUT_ATTRS = [
    "B",
    "BLOCKQUOTE",
    "CODE",
    "DD",
    "DL",
    "DT",
    "EM",
    "H1",
    "H2",
    "H3",
    "I",
    "LI",
    "OL",
    "PRE",
    "RP",
    "RT",
    "RUBY",
    "STRONG",
    "TABLE",
    "U",
    "UL",
];
for (const tag of TAGS_WITHOUT_ATTRS) {
    allowedTagsExtended[tag] = { attrs: [] };
}
allowedTagsBasic["IMG"] = { attrs: ["SRC"] };
allowedTagsExtended["A"] = { attrs: ["HREF"] };
allowedTagsExtended["TR"] = { attrs: ["ROWSPAN"] };
allowedTagsExtended["TD"] = { attrs: ["COLSPAN", "ROWSPAN"] };
allowedTagsExtended["TH"] = { attrs: ["COLSPAN", "ROWSPAN"] };
allowedTagsExtended["FONT"] = { attrs: ["COLOR"] };
const allowedStyling = {
    color: true,
    "background-color": true,
    "font-weight": true,
    "font-style": true,
    "text-decoration-line": true,
};
let isNightMode = function () {
    return document.body.classList.contains("nightMode");
};
let filterExternalSpan = function (node) {
    // filter out attributes
    let toRemove = [];
    for (const attr of node.attributes) {
        const attrName = attr.name.toUpperCase();
        if (attrName !== "STYLE") {
            toRemove.push(attr);
        }
    }
    for (const attributeToRemove of toRemove) {
        node.removeAttributeNode(attributeToRemove);
    }
    // filter styling
    toRemove = [];
    for (const name of node.style) {
        if (!allowedStyling.hasOwnProperty(name)) {
            toRemove.push(name);
        }
        if (name === "background-color" && node.style[name] === "transparent") {
            // google docs adds this unnecessarily
            toRemove.push(name);
        }
        if (isNightMode()) {
            // ignore coloured text in night mode for now
            if (name === "background-color" || name == "color") {
                toRemove.push(name);
            }
        }
    }
    for (let name of toRemove) {
        node.style.removeProperty(name);
    }
};
allowedTagsExtended["SPAN"] = filterExternalSpan;
// add basic tags to extended
Object.assign(allowedTagsExtended, allowedTagsBasic);
// filtering from another field
let filterInternalNode = function (node) {
    if (node.style) {
        node.style.removeProperty("background-color");
        node.style.removeProperty("font-size");
        node.style.removeProperty("font-family");
    }
    // recurse
    for (const child of node.childNodes) {
        filterInternalNode(child);
    }
};
// filtering from external sources
let filterNode = function (node, extendedMode) {
    // text node?
    if (node.nodeType === 3) {
        return;
    }
    // descend first, and take a copy of the child nodes as the loop will skip
    // elements due to node modifications otherwise
    const nodes = [];
    for (const child of node.childNodes) {
        nodes.push(child);
    }
    for (const child of nodes) {
        filterNode(child, extendedMode);
    }
    if (node.tagName === "ANKITOP") {
        return;
    }
    let tag;
    if (extendedMode) {
        tag = allowedTagsExtended[node.tagName];
    }
    else {
        tag = allowedTagsBasic[node.tagName];
    }
    if (!tag) {
        if (!node.innerHTML || node.tagName === "TITLE") {
            node.parentNode.removeChild(node);
        }
        else {
            node.outerHTML = node.innerHTML;
        }
    }
    else {
        if (typeof tag === "function") {
            // filtering function provided
            tag(node);
        }
        else {
            // allowed, filter out attributes
            const toRemove = [];
            for (const attr of node.attributes) {
                const attrName = attr.name.toUpperCase();
                if (tag.attrs.indexOf(attrName) === -1) {
                    toRemove.push(attr);
                }
            }
            for (const attributeToRemove of toRemove) {
                node.removeAttributeNode(attributeToRemove);
            }
        }
    }
};
let adjustFieldsTopMargin = function () {
    const topHeight = $("#topbuts").height();
    const margin = topHeight + 8;
    document.getElementById("fields").style.marginTop = margin + "px";
};
let mouseDown = 0;
$(function () {
    document.body.onmousedown = function () {
        mouseDown++;
    };
    document.body.onmouseup = function () {
        mouseDown--;
    };
    document.onclick = function (evt) {
        const src = evt.target;
        if (src.tagName === "IMG") {
            // image clicked; find contenteditable parent
            let p = src;
            while ((p = p.parentNode)) {
                if (p.className === "field") {
                    $("#" + p.id).focus();
                    break;
                }
            }
        }
    };
    // prevent editor buttons from taking focus
    $("button.linkb").on("mousedown", function (e) {
        e.preventDefault();
    });
    window.onresize = function () {
        adjustFieldsTopMargin();
    };
    adjustFieldsTopMargin();
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZWRpdG9yLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vLi4vLi4vLi4vLi4vLi4vLi4vLi4vcXQvYXF0L2RhdGEvd2ViL2pzL2VkaXRvci50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUE7a0ZBQ2tGO0FBRWxGLElBQUksWUFBWSxHQUFHLElBQUksQ0FBQztBQUN4QixJQUFJLFdBQVcsR0FBRyxJQUFJLENBQUM7QUFDdkIsSUFBSSxhQUFhLEdBQUcsSUFBSSxDQUFDO0FBTXpCLHlDQUF5QztBQUN6QyxNQUFNLENBQUMsU0FBUyxDQUFDLE1BQU0sR0FBRztJQUN0QixNQUFNLElBQUksR0FBRyxTQUFTLENBQUM7SUFDdkIsT0FBTyxJQUFJLENBQUMsT0FBTyxDQUFDLFVBQVUsRUFBRSxVQUFVLENBQUM7UUFDdkMsT0FBTyxJQUFJLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDO0lBQ2hDLENBQUMsQ0FBQyxDQUFDO0FBQ1AsQ0FBQyxDQUFDO0FBRUYsU0FBUyxXQUFXLENBQUMsR0FBRztJQUNwQixDQUFDLENBQUMsWUFBWSxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsS0FBSyxDQUFDLGVBQWUsR0FBRyxHQUFHLENBQUM7QUFDbkQsQ0FBQztBQUVELFNBQVMsT0FBTyxDQUFDLFNBQVM7SUFDdEIsSUFBSSxDQUFDLFlBQVksRUFBRTtRQUNmLE9BQU87S0FDVjtJQUVELGdCQUFnQixFQUFFLENBQUM7SUFFbkIsSUFBSSxTQUFTLEVBQUU7UUFDWCxTQUFTLENBQUMsS0FBSyxDQUFDLENBQUM7S0FDcEI7U0FBTTtRQUNILCtCQUErQjtRQUMvQixZQUFZLENBQUMsSUFBSSxFQUFFLENBQUM7S0FDdkI7QUFDTCxDQUFDO0FBRUQsU0FBUyxlQUFlO0lBQ3BCLGdCQUFnQixFQUFFLENBQUM7SUFDbkIsV0FBVyxHQUFHLFVBQVUsQ0FBQztRQUNyQixpQkFBaUIsRUFBRSxDQUFDO1FBQ3BCLFNBQVMsQ0FBQyxLQUFL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LENBQUMsQ0FBQztBQUVGLElBQUksU0FBUyxHQUFHLENBQUMsQ0FBQztBQUVsQixDQUFDLENBQUM7SUFDRSxRQUFRLENBQUMsSUFBSSxDQUFDLFdBQVcsR0FBRztRQUN4QixTQUFTLEVBQUUsQ0FBQztJQUNoQixDQUFDLENBQUM7SUFFRixRQUFRLENBQUMsSUFBSSxDQUFDLFNBQVMsR0FBRztRQUN0QixTQUFTLEVBQUUsQ0FBQztJQUNoQixDQUFDLENBQUM7SUFFRixRQUFRLENBQUMsT0FBTyxHQUFHLFVBQVUsR0FBZTtRQUN4QyxNQUFNLEdBQUcsR0FBRyxHQUFHLENBQUMsTUFBaUIsQ0FBQztRQUNsQyxJQUFJLEdBQUcsQ0FBQyxPQUFPLEtBQUssS0FBSyxFQUFFO1lBQ3ZCLDZDQUE2QztZQUM3QyxJQUFJLENBQUMsR0FBRyxHQUFHLENBQUM7WUFDWixPQUFPLENBQUMsQ0FBQyxHQUFHLENBQUMsQ0FBQyxVQUFxQixDQUFDLEVBQUU7Z0JBQ2xDLElBQUksQ0FBQyxDQUFDLFNBQVMsS0FBSyxPQUFPLEVBQUU7b0JBQ3pCLENBQUMsQ0FBQyxHQUFHLEdBQUcsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxDQUFDLEtBQUssRUFBRSxDQUFDO29CQUN0QixNQUFNO2lCQUNUO2FBQ0o7U0FDSjtJQUNMLENBQUMsQ0FBQztJQUVGLDJDQUEyQztJQUMzQyxDQUFDLENBQUMsY0FBYyxDQUFDLENBQUMsRUFBRSxDQUFDLFdBQVcsRUFBRSxVQUFVLENBQUM7UUFDekMsQ0FBQyxDQUFDLGNBQWMsRUFBRSxDQUFDO0lBQ3ZCLENBQUMsQ0FBQyxDQUFDO0lBRUgsTUFBTSxDQUFDLFFBQVEsR0FBRztRQUNkLHFCQUFxQixFQUFFLENBQUM7SUFDNUIsQ0FBQyxDQUFDO0lBRUYscUJBQXFCLEVBQUUsQ0FBQztBQUM1QixDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbIi8qIENvcHlyaWdodDogQW5raXRlY3RzIFB0eSBMdGQgYW5kIGNvbnRyaWJ1dG9yc1xuICogTGljZW5zZTogR05VIEFHUEwsIHZlcnNpb24gMyBvciBsYXRlcjsgaHR0cDovL3d3dy5nbnUub3JnL2xpY2Vuc2VzL2FncGwuaHRtbCAqL1xuXG5sZXQgY3VycmVudEZpZWxkID0gbnVsbDtcbmxldCBjaGFuZ2VUaW1lciA9IG51bGw7XG5sZXQgY3VycmVudE5vdGVJZCA9IG51bGw7XG5cbmRlY2xhcmUgaW50ZXJmYWNlIFN0cmluZyB7XG4gICAgZm9ybWF0KC4uLmFyZ3MpOiBzdHJpbmc7XG59XG5cbi8qIGtlcHQgZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBhZGQtb25zICovXG5TdHJpbmcucHJvdG90eXBlLmZvcm1hdCA9IGZ1bmN0aW9uICgpIHtcbiAgICBjb25zdCBhcmdzID0gYXJndW1lbnRzO1xuICAgIHJldHVybiB0aGlzLnJlcGxhY2UoL1xce1xcZCtcXH0vZywgZnVuY3Rpb24gKG0pIHtcbiAgICAgICAgcmV0dXJuIGFyZ3NbbS5tYXRjaCgvXFxkKy8pXTtcbiAgICB9KTtcbn07XG5cbmZ1bmN0aW9uIHNldEZHQnV0dG9uKGNvbCkge1xuICAgICQoXCIjZm9yZWNvbG9yXCIpWzBdLnN0eWxlLmJhY2tncm91bmRDb2xvciA9IGNvbDtcbn1cblxuZnVuY3Rpb24gc2F2ZU5vdyhrZWVwRm9jdXMpIHtcbiAgICBpZiAoIWN1cnJlbnRGaWVsZCkge1xuICAgICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY2xlYXJDaGFuZ2VUaW1lcigpO1xuXG4gICAgaWYgKGtlZXBGb2N1cykge1xuICAgICAgICBzYXZlRmllbGQoXCJrZXlcIik7XG4gICAgfSBlbHNlIHtcbiAgICAgICAgLy8gdHJpZ2dlcnMgb25CbHVyLCB3aGljaCBzYXZlc1xuICAgICAgICBjdXJyZW50RmllbGQuYmx1cigpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gdHJpZ2dlcktleVRpbWVyKCkge1xuICAgIGNsZWFyQ2hhbmdlVGltZXIoKTtcbiAgICBjaGFuZ2VUaW1lciA9IHNldFRpbWVvdXQoZnVuY3Rpb24gKCkge1xuICAgICAgICB1cGRhdGVCdXR0b25TdGF0ZSgpO1xuICAgICAgICBzYXZlRmllbGQoXCJrZXlcIik7XG4gICAgfSwgNjAwKTtcbn1cblxuaW50ZXJmYWNlIFNlbGVjdGlvbiB7XG4gICAgbW9kaWZ5KHM6IHN0cmluZywgdDogc3RyaW5nLCB1OiBzdHJpbmcpOiB2b2lkO1xufVxuXG5mdW5jdGlvbiBvbktleShldnQ6IEtleWJvYXJkRXZlbnQpIHtcbiAgICAvLyBlc2MgY2xlYXJzIGZvY3VzLCBhbGxvd2luZyBkaWFsb2cgdG8gY2xvc2VcbiAgICBpZiAoZXZ0LndoaWNoID09PSAyNykge1xuICAgICAgICBjdXJyZW50RmllbGQuYmx1cigpO1xuICAgICAgICByZXR1cm47XG4gICAgfVxuICAgIC8vIHNoaWZ0K3RhYiBnb2VzIHRvIHByZXZpb3VzIGZpZWxkXG4gICAgaWYgKG5hdmlnYXRvci5wbGF0Zm9ybSA9PT0gXCJNYWNJbnRlbFwiICYmIGV2dC53aGljaCA9PT0gOSAmJiBldnQuc2hpZnRLZXkpIHtcbiAgICAgICAgZXZ0LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgIGZvY3VzUHJldmlvdXMoKTtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIC8vIGZpeCBDdHJsK3JpZ2h0L2xlZnQgaGFuZGxpbmcgaW4gUlRMIGZpZWxkc1xuICAgIGlmIChjdXJyZW50RmllbGQuZGlyID09PSBcInJ0bFwiKSB7XG4gICAgICAgIGNvbnN0IHNlbGVjdGlvbiA9IHdpbmRvdy5nZXRTZWxlY3Rpb24oKTtcbiAgICAgICAgbGV0IGdyYW51bGFyaXR5ID0gXCJjaGFyYWN0ZXJcIjtcbiAgICAgICAgbGV0IGFsdGVyID0gXCJtb3ZlXCI7XG4gICAgICAgIGlmIChldnQuY3RybEtleSkge1xuICAgICAgICAgICAgZ3JhbnVsYXJpdHkgPSBcIndvcmRcIjtcbiAgICAgICAgfVxuICAgICAgICBpZiAoZXZ0LnNoaWZ0S2V5KSB7XG4gICAgICAgICAgICBhbHRlciA9IFwiZXh0ZW5kXCI7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGV2dC53aGljaCA9PT0gMzkpIHtcbiAgICAgICAgICAgIHNlbGVjdGlvbi5tb2RpZnkoYWx0ZXIsIFwicmlnaHRcIiwgZ3JhbnVsYXJpdHkpO1xuICAgICAgICAgICAgZXZ0LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIH0gZWxzZSBpZiAoZXZ0LndoaWNoID09PSAzNykge1xuICAgICAgICAgICAgc2VsZWN0aW9uLm1vZGlmeShhbHRlciwgXCJsZWZ0XCIsIGdyYW51bGFyaXR5KTtcbiAgICAgICAgICAgIGV2dC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgdHJpZ2dlcktleVRpbWVyKCk7XG59XG5cbmZ1bmN0aW9uIGluc2VydE5ld2xpbmUoKSB7XG4gICAgaWYgKCFpblByZUVudmlyb25tZW50KCkpIHtcbiAgICAgICAgc2V0Rm9ybWF0KFwiaW5zZXJ0VGV4dFwiLCBcIlxcblwiKTtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIC8vIGluIHNvbWUgY2FzZXMgaW5zZXJ0aW5nIGEgbmV3bGluZSB3aWxsIG5vdCBzaG93IGFueSBjaGFuZ2VzLFxuICAgIC8vIGFzIGEgdHJhaWxpbmcgbmV3bGluZSBhdCB0aGUgZW5kIG9mIGEgYmxvY2sgZG9lcyBub3QgcmVuZGVyXG4gICAgLy8gZGlmZmVyZW50bHkuIHNvIGluIHN1Y2ggY2FzZXMgd2Ugbm90ZSB0aGUgaGVpZ2h0IGhhcyBub3RcbiAgICAvLyBjaGFuZ2VkIGFuZCBpbnNlcnQgYW4gZXh0cmEgbmV3bGluZS5cblxuICAgIGNvbnN0IHIgPSB3aW5kb3cuZ2V0U2VsZWN0aW9uKCkuZ2V0UmFuZ2VBdCgwKTtcbiAgICBpZiAoIXIuY29sbGFwc2VkKSB7XG4gICAgICAgIC8vIGRlbGV0ZSBhbnkgY3VycmVudGx5IHNlbGVjdGVkIHRleHQgZmlyc3QsIG1ha2luZ1xuICAgICAgICAvLyBzdXJlIHRoZSBkZWxldGUgaXMgdW5kb2FibGVcbiAgICAgICAgc2V0Rm9ybWF0KFwiZGVsZXRlXCIpO1xuICAgIH1cblxuICAgIGNvbnN0IG9sZEhlaWdodCA9IGN1cnJlbnRGaWVsZC5jbGllbnRIZWlnaHQ7XG4gICAgc2V0Rm9ybWF0KFwiaW5zZXJ0aHRtbFwiLCBcIlxcblwiKTtcbiAgICBpZiAoY3VycmVudEZpZWxkLmNsaWVudEhlaWdodCA9PT0gb2xkSGVpZ2h0KSB7XG4gICAgICAgIHNldEZvcm1hdChcImluc2VydGh0bWxcIiwgXCJcXG5cIik7XG4gICAgfVxufVxuXG4vLyBpcyB0aGUgY3Vyc29yIGluIGFuIGVudmlyb25tZW50IHRoYXQgcmVzcGVjdHMgd2hpdGVzcGFjZT9cbmZ1bmN0aW9uIGluUHJlRW52aXJvbm1lbnQoKSB7XG4gICAgbGV0IG4gPSB3aW5kb3cuZ2V0U2VsZWN0aW9uKCkuYW5jaG9yTm9kZSBhcyBFbGVtZW50O1xuICAgIGlmIChuLm5vZGVUeXBlID09PSAzKSB7XG4gICAgICAgIG4gPSBuLnBhcmVudE5vZGUgYXMgRWxlbWVudDtcbiAgICB9XG4gICAgcmV0dXJuIHdpbmRvdy5nZXRDb21wdXRlZFN0eWxlKG4pLndoaXRlU3BhY2Uuc3RhcnRzV2l0aChcInByZVwiKTtcbn1cblxuZnVuY3Rpb24gb25JbnB1dCgpIHtcbiAgICAvLyBlbXB0eSBmaWVsZD9cbiAgICBpZiAoY3VycmVudEZpZWxkLmlubmVySFRNTCA9PT0gXCJcIikge1xuICAgICAgICBjdXJyZW50RmllbGQuaW5uZXJIVE1MID0gXCI8YnI+XCI7XG4gICAgfVxuXG4gICAgLy8gbWFrZSBzdXJlIElNRSBjaGFuZ2VzIGdldCBzYXZlZFxuICAgIHRyaWdnZXJLZXlUaW1lcigpO1xufVxuXG5mdW5jdGlvbiB1cGRhdGVCdXR0b25TdGF0ZSgpIHtcbiAgICBjb25zdCBidXRzID0gW1wiYm9sZFwiLCBcIml0YWxpY1wiLCBcInVuZGVybGluZVwiLCBcInN1cGVyc2NyaXB0XCIsIFwic3Vic2NyaXB0XCJdO1xuICAgIGZvciAoY29uc3QgbmFtZSBvZiBidXRzKSB7XG4gICAgICAgIGlmIChkb2N1bWVudC5xdWVyeUNvbW1hbmRTdGF0ZShuYW1lKSkge1xuICAgICAgICAgICAgJChcIiNcIiArIG5hbWUpLmFkZENsYXNzKFwiaGlnaGxpZ2h0ZWRcIik7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAkKFwiI1wiICsgbmFtZSkucmVtb3ZlQ2xhc3MoXCJoaWdobGlnaHRlZFwiKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIC8vIGZpeG1lOiBmb3JlY29sb3JcbiAgICAvLyAgICAnY29sJzogZG9jdW1lbnQucXVlcnlDb21tYW5kVmFsdWUoXCJmb3JlY29sb3JcIilcbn1cblxuZnVuY3Rpb24gdG9nZ2xlRWRpdG9yQnV0dG9uKGJ1dHRvbmlkKSB7XG4gICAgaWYgKCQoYnV0dG9uaWQpLmhhc0NsYXNzKFwiaGlnaGxpZ2h0ZWRcIikpIHtcbiAgICAgICAgJChidXR0b25pZCkucmVtb3ZlQ2xhc3MoXCJoaWdobGlnaHRlZFwiKTtcbiAgICB9IGVsc2Uge1xuICAgICAgICAkKGJ1dHRvbmlkKS5hZGRDbGFzcyhcImhpZ2hsaWdodGVkXCIpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gc2V0Rm9ybWF0KGNtZDogc3RyaW5nLCBhcmc/OiBhbnksIG5vc2F2ZTogYm9vbGVhbiA9IGZhbHNlKSB7XG4gICAgZG9jdW1lbnQuZXhlY0NvbW1hbmQoY21kLCBmYWxzZSwgYXJnKTtcbiAgICBpZiAoIW5vc2F2ZSkge1xuICAgICAgICBzYXZlRmllbGQoXCJrZXlcIik7XG4gICAgICAgIHVwZGF0ZUJ1dHRvblN0YXRlKCk7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBjbGVhckNoYW5nZVRpbWVyKCkge1xuICAgIGlmIChjaGFuZ2VUaW1lcikge1xuICAgICAgICBjbGVhclRpbWVvdXQoY2hhbmdlVGltZXIpO1xuICAgICAgICBjaGFuZ2VUaW1lciA9IG51bGw7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBvbkZvY3VzKGVsZW0pIHtcbiAgICBpZiAoY3VycmVudEZpZWxkID09PSBlbGVtKSB7XG4gICAgICAgIC8vIGFua2kgd2luZG93IHJlZm9jdXNlZDsgY3VycmVudCBlbGVtZW50IHVuY2hhbmdlZFxuICAgICAgICByZXR1cm47XG4gICAgfVxuICAgIGN1cnJlbnRGaWVsZCA9IGVsZW07XG4gICAgcHljbWQoXCJmb2N1czpcIiArIGN1cnJlbnRGaWVsZE9yZGluYWwoKSk7XG4gICAgZW5hYmxlQnV0dG9ucygpO1xuICAgIC8vIGRvbid0IGFkanVzdCBjdXJzb3Igb24gbW91c2UgY2xpY2tzXG4gICAgaWYgKG1vdXNlRG93bikge1xuICAgICAgICByZXR1cm47XG4gICAgfVxuICAgIC8vIGRvIHRoaXMgdHdpY2Ugc28gdGhhdCB0aGVyZSdzIG5vIGZsaWNrZXIgb24gbmV3ZXIgdmVyc2lvbnNcbiAgICBjYXJldFRvRW5kKCk7XG4gICAgLy8gc2Nyb2xsIGlmIGJvdHRvbSBvZiBlbGVtZW50IG9mZiB0aGUgc2NyZWVuXG4gICAgZnVuY3Rpb24gcG9zKG9iaikge1xuICAgICAgICBsZXQgY3VyID0gMDtcbiAgICAgICAgZG8ge1xuICAgICAgICAgICAgY3VyICs9IG9iai5vZmZzZXRUb3A7XG4gICAgICAgIH0gd2hpbGUgKChvYmogPSBvYmoub2Zmc2V0UGFyZW50KSk7XG4gICAgICAgIHJldHVybiBjdXI7XG4gICAgfVxuXG4gICAgY29uc3QgeSA9IHBvcyhlbGVtKTtcbiAgICBpZiAoXG4gICAgICAgIHdpbmRvdy5wYWdlWU9mZnNldCArIHdpbmRvdy5pbm5lckhlaWdodCA8IHkgKyBlbGVtLm9mZnNldEhlaWdodCB8fFxuICAgICAgICB3aW5kb3cucGFnZVlPZmZzZXQgPiB5XG4gICAgKSB7XG4gICAgICAgIHdpbmRvdy5zY3JvbGwoMCwgeSArIGVsZW0ub2Zmc2V0SGVpZ2h0IC0gd2luZG93LmlubmVySGVpZ2h0KTtcbiAgICB9XG59XG5cbmZ1bmN0aW9uIGZvY3VzRmllbGQobikge1xuICAgIGlmIChuID09PSBudWxsKSB7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gICAgJChcIiNmXCIgKyBuKS5mb2N1cygpO1xufVxuXG5mdW5jdGlvbiBmb2N1c1ByZXZpb3VzKCkge1xuICAgIGlmICghY3VycmVudEZpZWxkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgcHJldmlvdXMgPSBjdXJyZW50RmllbGRPcmRpbmFsKCkgLSAxO1xuICAgIGlmIChwcmV2aW91cyA+PSAwKSB7XG4gICAgICAgIGZvY3VzRmllbGQocHJldmlvdXMpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gZm9jdXNJZkZpZWxkKHgsIHkpIHtcbiAgICBjb25zdCBlbGVtZW50cyA9IGRvY3VtZW50LmVsZW1lbnRzRnJvbVBvaW50KHgsIHkpO1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgZWxlbWVudHMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgbGV0IGVsZW0gPSBlbGVtZW50c1tpXSBhcyBIVE1MRWxlbWVudDtcbiAgICAgICAgaWYgKGVsZW0uY2xhc3NMaXN0LmNvbnRhaW5zKFwiZmllbGRcIikpIHtcbiAgICAgICAgICAgIGVsZW0uZm9jdXMoKTtcbiAgICAgICAgICAgIC8vIHRoZSBmb2N1cyBldmVudCBtYXkgbm90IGZpcmUgaWYgdGhlIHdpbmRvdyBpcyBub3QgYWN0aXZlLCBzbyBtYWtlIHN1cmVcbiAgICAgICAgICAgIC8vIHRoZSBjdXJyZW50IGZpZWxkIGlzIHNldFxuICAgICAgICAgICAgY3VycmVudEZpZWxkID0gZWxlbTtcbiAgICAgICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgICB9XG4gICAgfVxuICAgIHJldHVybiBmYWxzZTtcbn1cblxuZnVuY3Rpb24gb25QYXN0ZShlbGVtKSB7XG4gICAgcHljbWQoXCJwYXN0ZVwiKTtcbiAgICB3aW5kb3cuZXZlbnQucHJldmVudERlZmF1bHQoKTtcbn1cblxuZnVuY3Rpb24gY2FyZXRUb0VuZCgpIHtcbiAgICBjb25zdCByID0gZG9jdW1lbnQuY3JlYXRlUmFuZ2UoKTtcbiAgICByLnNlbGVjdE5vZGVDb250ZW50cyhjdXJyZW50RmllbGQpO1xuICAgIHIuY29sbGFwc2UoZmFsc2UpO1xuICAgIGNvbnN0IHMgPSBkb2N1bWVudC5nZXRTZWxlY3Rpb24oKTtcbiAgICBzLnJlbW92ZUFsbFJhbmdlcygpO1xuICAgIHMuYWRkUmFuZ2Uocik7XG59XG5cbmZ1bmN0aW9uIG9uQmx1cigpIHtcbiAgICBpZiAoIWN1cnJlbnRGaWVsZCkge1xuICAgICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgaWYgKGRvY3VtZW50LmFjdGl2ZUVsZW1lbnQgPT09IGN1cnJlbnRGaWVsZCkge1xuICAgICAgICAvLyBvdGhlciB3aWRnZXQgb3Igd2luZG93IGZvY3VzZWQ7IGN1cnJlbnQgZmllbGQgdW5jaGFuZ2VkXG4gICAgICAgIHNhdmVGaWVsZChcImtleVwiKTtcbiAgICB9IGVsc2Uge1xuICAgICAgICBzYXZlRmllbGQoXCJibHVyXCIpO1xuICAgICAgICBjdXJyZW50RmllbGQgPSBudWxsO1xuICAgICAgICBkaXNhYmxlQnV0dG9ucygpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gc2F2ZUZpZWxkKHR5cGUpIHtcbiAgICBjbGVhckNoYW5nZVRpbWVyKCk7XG4gICAgaWYgKCFjdXJyZW50RmllbGQpIHtcbiAgICAgICAgLy8gbm8gZmllbGQgaGFzIGJlZW4gZm9jdXNlZCB5ZXRcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICAvLyB0eXBlIGlzIGVpdGhlciAnYmx1cicgb3IgJ2tleSdcbiAgICBweWNtZChcbiAgICAgICAgdHlwZSArXG4gICAgICAgICAgICBcIjpcIiArXG4gICAgICAgICAgICBjdXJyZW50RmllbGRPcmRpbmFsKCkgK1xuICAgICAgICAgICAgXCI6XCIgK1xuICAgICAgICAgICAgY3VycmVudE5vdGVJZCArXG4gICAgICAgICAgICBcIjpcIiArXG4gICAgICAgICAgICBjdXJyZW50RmllbGQuaW5uZXJIVE1MXG4gICAgKTtcbn1cblxuZnVuY3Rpb24gY3VycmVudEZpZWxkT3JkaW5hbCgpIHtcbiAgICByZXR1cm4gY3VycmVudEZpZWxkLmlkLnN1YnN0cmluZygxKTtcbn1cblxuZnVuY3Rpb24gd3JhcHBlZEV4Y2VwdEZvcldoaXRlc3BhY2UodGV4dCwgZnJvbnQsIGJhY2spIHtcbiAgICBjb25zdCBtYXRjaCA9IHRleHQubWF0Y2goL14oXFxzKikoW15dKj8pKFxccyopJC8pO1xuICAgIHJldHVybiBtYXRjaFsxXSArIGZyb250ICsgbWF0Y2hbMl0gKyBiYWNrICsgbWF0Y2hbM107XG59XG5cbmZ1bmN0aW9uIGRpc2FibGVCdXR0b25zKCkge1xuICAgICQoXCJidXR0b24ubGlua2I6bm90KC5wZXJtKVwiKS5wcm9wKFwiZGlzYWJsZWRcIiwgdHJ1ZSk7XG59XG5cbmZ1bmN0aW9uIGVuYWJsZUJ1dHRvbnMoKSB7XG4gICAgJChcImJ1dHRvbi5saW5rYlwiKS5wcm9wKFwiZGlzYWJsZWRcIiwgZmFsc2UpO1xufVxuXG4vLyBkaXNhYmxlIHRoZSBidXR0b25zIGlmIGEgZmllbGQgaXMgbm90IGN1cnJlbnRseSBmb2N1c2VkXG5mdW5jdGlvbiBtYXliZURpc2FibGVCdXR0b25zKCkge1xuICAgIGlmICghZG9jdW1lbnQuYWN0aXZlRWxlbWVudCB8fCBkb2N1bWVudC5hY3RpdmVFbGVtZW50LmNsYXNzTmFtZSAhPT0gXCJmaWVsZFwiKSB7XG4gICAgICAgIGRpc2FibGVCdXR0b25zKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgICAgZW5hYmxlQnV0dG9ucygpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gd3JhcChmcm9udCwgYmFjaykge1xuICAgIHdyYXBJbnRlcm5hbChmcm9udCwgYmFjaywgZmFsc2UpO1xufVxuXG4vKiBjdXJyZW50bHkgdW51c2VkICovXG5mdW5jdGlvbiB3cmFwSW50b1RleHQoZnJvbnQsIGJhY2spIHtcbiAgICB3cmFwSW50ZXJuYWwoZnJvbnQsIGJhY2ssIHRydWUpO1xufVxuXG5mdW5jdGlvbiB3cmFwSW50ZXJuYWwoZnJvbnQsIGJhY2ssIHBsYWluVGV4dCkge1xuICAgIGNvbnN0IHMgPSB3aW5kb3cuZ2V0U2VsZWN0aW9uKCk7XG4gICAgbGV0IHIgPSBzLmdldFJhbmdlQXQoMCk7XG4gICAgY29uc3QgY29udGVudCA9IHIuY2xvbmVDb250ZW50cygpO1xuICAgIGNvbnN0IHNwYW4gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwic3BhblwiKTtcbiAgICBzcGFuLmFwcGVuZENoaWxkKGNvbnRlbnQpO1xuICAgIGlmIChwbGFpblRleHQpIHtcbiAgICAgICAgY29uc3QgbmV3XyA9IHdyYXBwZWRFeGNlcHRGb3JXaGl0ZXNwYWNlKHNwYW4uaW5uZXJUZXh0LCBmcm9udCwgYmFjayk7XG4gICAgICAgIHNldEZvcm1hdChcImluc2VydHRleHRcIiwgbmV3Xyk7XG4gICAgfSBlbHNlIHtcbiAgICAgICAgY29uc3QgbmV3XyA9IHdyYXBwZWRFeGNlcHRGb3JXaGl0ZXNwYWNlKHNwYW4uaW5uZXJIVE1MLCBmcm9udCwgYmFjayk7XG4gICAgICAgIHNldEZvcm1hdChcImluc2VydGh0bWxcIiwgbmV3Xyk7XG4gICAgfVxuICAgIGlmICghc3Bhbi5pbm5lckhUTUwpIHtcbiAgICAgICAgLy8gcnVuIHdpdGggYW4gZW1wdHkgc2VsZWN0aW9uOyBtb3ZlIGN1cnNvciBiYWNrIHBhc3QgcG9zdGZpeFxuICAgICAgICByID0gcy5nZXRSYW5nZUF0KDApO1xuICAgICAgICByLnNldFN0YXJ0KHIuc3RhcnRDb250YWluZXIsIHIuc3RhcnRPZmZzZXQgLSBiYWNrLmxlbmd0aCk7XG4gICAgICAgIHIuY29sbGFwc2UodHJ1ZSk7XG4gICAgICAgIHMucmVtb3ZlQWxsUmFuZ2VzKCk7XG4gICAgICAgIHMuYWRkUmFuZ2Uocik7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBvbkN1dE9yQ29weSgpIHtcbiAgICBweWNtZChcImN1dE9yQ29weVwiKTtcbiAgICByZXR1cm4gdHJ1ZTtcbn1cblxuZnVuY3Rpb24gc2V0RmllbGRzKGZpZWxkcykge1xuICAgIGxldCB0eHQgPSBcIlwiO1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgZmllbGRzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIGNvbnN0IG4gPSBmaWVsZHNbaV1bMF07XG4gICAgICAgIGxldCBmID0gZmllbGRzW2ldWzFdO1xuICAgICAgICBpZiAoIWYpIHtcbiAgICAgICAgICAgIGYgPSBcIjxicj5cIjtcbiAgICAgICAgfVxuICAgICAgICB0eHQgKz0gYFxuICAgICAgICA8dHI+XG4gICAgICAgICAgICA8dGQgY2xhc3M9Zm5hbWUgaWQ9XCJuYW1lJHtpfVwiPiR7bn08L3RkPlxuICAgICAgICA8L3RyPlxuICAgICAgICA8dHI+XG4gICAgICAgICAgICA8dGQgd2lkdGg9MTAwJT5cbiAgICAgICAgICAgICAgICA8ZGl2IGlkPWYke2l9XG4gICAgICAgICAgICAgICAgICAgICBvbmtleWRvd249J29uS2V5KHdpbmRvdy5ldmVudCk7J1xuICAgICAgICAgICAgICAgICAgICAgb25pbnB1dD0nb25JbnB1dCgpOydcbiAgICAgICAgICAgICAgICAgICAgIG9ubW91c2V1cD0nb25LZXkod2luZG93LmV2ZW50KTsnXG4gICAgICAgICAgICAgICAgICAgICBvbmZvY3VzPSdvbkZvY3VzKHRoaXMpOydcbiAgICAgICAgICAgICAgICAgICAgIG9uYmx1cj0nb25CbHVyKCk7J1xuICAgICAgICAgICAgICAgICAgICAgY2xhc3M9J2ZpZWxkIGNsZWFyZml4J1xuICAgICAgICAgICAgICAgICAgICAgb25wYXN0ZT0nb25QYXN0ZSh0aGlzKTsnXG4gICAgICAgICAgICAgICAgICAgICBvbmNvcHk9J29uQ3V0T3JDb3B5KHRoaXMpOydcbiAgICAgICAgICAgICAgICAgICAgIG9uY3V0PSdvbkN1dE9yQ29weSh0aGlzKTsnXG4gICAgICAgICAgICAgICAgICAgICBjb250ZW50RWRpdGFibGU9dHJ1ZVxuICAgICAgICAgICAgICAgICAgICAgY2xhc3M9ZmllbGRcbiAgICAgICAgICAgICAgICA+JHtmfTwvZGl2PlxuICAgICAgICAgICAgPC90ZD5cbiAgICAgICAgPC90cj5gO1xuICAgIH1cbiAgICAkKFwiI2ZpZWxkc1wiKS5odG1sKGBcbiAgICA8dGFibGUgY2VsbHBhZGRpbmc9MCB3aWR0aD0xMDAlIHN0eWxlPSd0YWJsZS1sYXlvdXQ6IGZpeGVkOyc+XG4ke3R4dH1cbiAgICA8L3RhYmxlPmApO1xuICAgIG1heWJlRGlzYWJsZUJ1dHRvbnMoKTtcbn1cblxuZnVuY3Rpb24gc2V0QmFja2dyb3VuZHMoY29scykge1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgY29scy5sZW5ndGg7IGkrKykge1xuICAgICAgICBpZiAoY29sc1tpXSA9PSBcImR1cGVcIikge1xuICAgICAgICAgICAgJChcIiNmXCIgKyBpKS5hZGRDbGFzcyhcImR1cGVcIik7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAkKFwiI2ZcIiArIGkpLnJlbW92ZUNsYXNzKFwiZHVwZVwiKTtcbiAgICAgICAgfVxuICAgIH1cbn1cblxuZnVuY3Rpb24gc2V0Rm9udHMoZm9udHMpIHtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IGZvbnRzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIGNvbnN0IG4gPSAkKFwiI2ZcIiArIGkpO1xuICAgICAgICBuLmNzcyhcImZvbnQtZmFtaWx5XCIsIGZvbnRzW2ldWzBdKS5jc3MoXCJmb250LXNpemVcIiwgZm9udHNbaV1bMV0pO1xuICAgICAgICBuWzBdLmRpciA9IGZvbnRzW2ldWzJdID8gXCJydGxcIiA6IFwibHRyXCI7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBzZXROb3RlSWQoaWQpIHtcbiAgICBjdXJyZW50Tm90ZUlkID0gaWQ7XG59XG5cbmZ1bmN0aW9uIHNob3dEdXBlcygpIHtcbiAgICAkKFwiI2R1cGVzXCIpLnNob3coKTtcbn1cblxuZnVuY3Rpb24gaGlkZUR1cGVzKCkge1xuICAgICQoXCIjZHVwZXNcIikuaGlkZSgpO1xufVxuXG4vLy8gSWYgdGhlIGZpZWxkIGhhcyBvbmx5IGFuIGVtcHR5IGJyLCByZW1vdmUgaXQgZmlyc3QuXG5sZXQgaW5zZXJ0SHRtbFJlbW92aW5nSW5pdGlhbEJSID0gZnVuY3Rpb24gKGh0bWw6IHN0cmluZykge1xuICAgIGlmIChodG1sICE9PSBcIlwiKSB7XG4gICAgICAgIC8vIHJlbW92ZSA8YnI+IGluIGVtcHR5IGZpZWxkXG4gICAgICAgIGlmIChjdXJyZW50RmllbGQgJiYgY3VycmVudEZpZWxkLmlubmVySFRNTCA9PT0gXCI8YnI+XCIpIHtcbiAgICAgICAgICAgIGN1cnJlbnRGaWVsZC5pbm5lckhUTUwgPSBcIlwiO1xuICAgICAgICB9XG4gICAgICAgIHNldEZvcm1hdChcImluc2VydGh0bWxcIiwgaHRtbCk7XG4gICAgfVxufTtcblxubGV0IHBhc3RlSFRNTCA9IGZ1bmN0aW9uIChodG1sLCBpbnRlcm5hbCwgZXh0ZW5kZWRNb2RlKSB7XG4gICAgaHRtbCA9IGZpbHRlckhUTUwoaHRtbCwgaW50ZXJuYWwsIGV4dGVuZGVkTW9kZSk7XG4gICAgaW5zZXJ0SHRtbFJlbW92aW5nSW5pdGlhbEJSKGh0bWwpO1xufTtcblxubGV0IGZpbHRlckhUTUwgPSBmdW5jdGlvbiAoaHRtbCwgaW50ZXJuYWwsIGV4dGVuZGVkTW9kZSkge1xuICAgIC8vIHdyYXAgaXQgaW4gPHRvcD4gYXMgd2UgYXJlbid0IGFsbG93ZWQgdG8gY2hhbmdlIHRvcCBsZXZlbCBlbGVtZW50c1xuICAgIGNvbnN0IHRvcCA9ICQucGFyc2VIVE1MKFwiPGFua2l0b3A+XCIgKyBodG1sICsgXCI8L2Fua2l0b3A+XCIpWzBdIGFzIEVsZW1lbnQ7XG4gICAgaWYgKGludGVybmFsKSB7XG4gICAgICAgIGZpbHRlckludGVybmFsTm9kZSh0b3ApO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIGZpbHRlck5vZGUodG9wLCBleHRlbmRlZE1vZGUpO1xuICAgIH1cbiAgICBsZXQgb3V0SHRtbCA9IHRvcC5pbm5lckhUTUw7XG4gICAgaWYgKCFleHRlbmRlZE1vZGUgJiYgIWludGVybmFsKSB7XG4gICAgICAgIC8vIGNvbGxhcHNlIHdoaXRlc3BhY2VcbiAgICAgICAgb3V0SHRtbCA9IG91dEh0bWwucmVwbGFjZSgvW1xcblxcdCBdKy9nLCBcIiBcIik7XG4gICAgfVxuICAgIG91dEh0bWwgPSBvdXRIdG1sLnRyaW0oKTtcbiAgICAvL2NvbnNvbGUubG9nKGBpbnB1dCBodG1sOiAke2h0bWx9YCk7XG4gICAgLy9jb25zb2xlLmxvZyhgb3V0cHQgaHRtbDogJHtvdXRIdG1sfWApO1xuICAgIHJldHVybiBvdXRIdG1sO1xufTtcblxubGV0IGFsbG93ZWRUYWdzQmFzaWMgPSB7fTtcbmxldCBhbGxvd2VkVGFnc0V4dGVuZGVkID0ge307XG5cbmxldCBUQUdTX1dJVEhPVVRfQVRUUlMgPSBbXCJQXCIsIFwiRElWXCIsIFwiQlJcIiwgXCJTVUJcIiwgXCJTVVBcIl07XG5mb3IgKGNvbnN0IHRhZyBvZiBUQUdTX1dJVEhPVVRfQVRUUlMpIHtcbiAgICBhbGxvd2VkVGFnc0Jhc2ljW3RhZ10gPSB7IGF0dHJzOiBbXSB9O1xufVxuXG5UQUdTX1dJVEhPVVRfQVRUUlMgPSBbXG4gICAgXCJCXCIsXG4gICAgXCJCTE9DS1FVT1RFXCIsXG4gICAgXCJDT0RFXCIsXG4gICAgXCJERFwiLFxuICAgIFwiRExcIixcbiAgICBcIkRUXCIsXG4gICAgXCJFTVwiLFxuICAgIFwiSDFcIixcbiAgICBcIkgyXCIsXG4gICAgXCJIM1wiLFxuICAgIFwiSVwiLFxuICAgIFwiTElcIixcbiAgICBcIk9MXCIsXG4gICAgXCJQUkVcIixcbiAgICBcIlJQXCIsXG4gICAgXCJSVFwiLFxuICAgIFwiUlVCWVwiLFxuICAgIFwiU1RST05HXCIsXG4gICAgXCJUQUJMRVwiLFxuICAgIFwiVVwiLFxuICAgIFwiVUxcIixcbl07XG5mb3IgKGNvbnN0IHRhZyBvZiBUQUdTX1dJVEhPVVRfQVRUUlMpIHtcbiAgICBhbGxvd2VkVGFnc0V4dGVuZGVkW3RhZ10gPSB7IGF0dHJzOiBbXSB9O1xufVxuXG5hbGxvd2VkVGFnc0Jhc2ljW1wiSU1HXCJdID0geyBhdHRyczogW1wiU1JDXCJdIH07XG5cbmFsbG93ZWRUYWdzRXh0ZW5kZWRbXCJBXCJdID0geyBhdHRyczogW1wiSFJFRlwiXSB9O1xuYWxsb3dlZFRhZ3NFeHRlbmRlZFtcIlRSXCJdID0geyBhdHRyczogW1wiUk9XU1BBTlwiXSB9O1xuYWxsb3dlZFRhZ3NFeHRlbmRlZFtcIlREXCJdID0geyBhdHRyczogW1wiQ09MU1BBTlwiLCBcIlJPV1NQQU5cIl0gfTtcbmFsbG93ZWRUYWdzRXh0ZW5kZWRbXCJUSFwiXSA9IHsgYXR0cnM6IFtcIkNPTFNQQU5cIiwgXCJST1dTUEFOXCJdIH07XG5hbGxvd2VkVGFnc0V4dGVuZGVkW1wiRk9OVFwiXSA9IHsgYXR0cnM6IFtcIkNPTE9SXCJdIH07XG5cbmNvbnN0IGFsbG93ZWRTdHlsaW5nID0ge1xuICAgIGNvbG9yOiB0cnVlLFxuICAgIFwiYmFja2dyb3VuZC1jb2xvclwiOiB0cnVlLFxuICAgIFwiZm9udC13ZWlnaHRcIjogdHJ1ZSxcbiAgICBcImZvbnQtc3R5bGVcIjogdHJ1ZSxcbiAgICBcInRleHQtZGVjb3JhdGlvbi1saW5lXCI6IHRydWUsXG59O1xuXG5sZXQgaXNOaWdodE1vZGUgPSBmdW5jdGlvbiAoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIGRvY3VtZW50LmJvZHkuY2xhc3NMaXN0LmNvbnRhaW5zKFwibmlnaHRNb2RlXCIpO1xufTtcblxubGV0IGZpbHRlckV4dGVybmFsU3BhbiA9IGZ1bmN0aW9uIChub2RlKSB7XG4gICAgLy8gZmlsdGVyIG91dCBhdHRyaWJ1dGVzXG4gICAgbGV0IHRvUmVtb3ZlID0gW107XG4gICAgZm9yIChjb25zdCBhdHRyIG9mIG5vZGUuYXR0cmlidXRlcykge1xuICAgICAgICBjb25zdCBhdHRyTmFtZSA9IGF0dHIubmFtZS50b1VwcGVyQ2FzZSgpO1xuICAgICAgICBpZiAoYXR0ck5hbWUgIT09IFwiU1RZTEVcIikge1xuICAgICAgICAgICAgdG9SZW1vdmUucHVzaChhdHRyKTtcbiAgICAgICAgfVxuICAgIH1cbiAgICBmb3IgKGNvbnN0IGF0dHJpYnV0ZVRvUmVtb3ZlIG9mIHRvUmVtb3ZlKSB7XG4gICAgICAgIG5vZGUucmVtb3ZlQXR0cmlidXRlTm9kZShhdHRyaWJ1dGVUb1JlbW92ZSk7XG4gICAgfVxuICAgIC8vIGZpbHRlciBzdHlsaW5nXG4gICAgdG9SZW1vdmUgPSBbXTtcbiAgICBmb3IgKGNvbnN0IG5hbWUgb2Ygbm9kZS5zdHlsZSkge1xuICAgICAgICBpZiAoIWFsbG93ZWRTdHlsaW5nLmhhc093blByb3BlcnR5KG5hbWUpKSB7XG4gICAgICAgICAgICB0b1JlbW92ZS5wdXNoKG5hbWUpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChuYW1lID09PSBcImJhY2tncm91bmQtY29sb3JcIiAmJiBub2RlLnN0eWxlW25hbWVdID09PSBcInRyYW5zcGFyZW50XCIpIHtcbiAgICAgICAgICAgIC8vIGdvb2dsZSBkb2NzIGFkZHMgdGhpcyB1bm5lY2Vzc2FyaWx5XG4gICAgICAgICAgICB0b1JlbW92ZS5wdXNoKG5hbWUpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChpc05pZ2h0TW9kZSgpKSB7XG4gICAgICAgICAgICAvLyBpZ25vcmUgY29sb3VyZWQgdGV4dCBpbiBuaWdodCBtb2RlIGZvciBub3dcbiAgICAgICAgICAgIGlmIChuYW1lID09PSBcImJhY2tncm91bmQtY29sb3JcIiB8fCBuYW1lID09IFwiY29sb3JcIikge1xuICAgICAgICAgICAgICAgIHRvUmVtb3ZlLnB1c2gobmFtZSk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9XG4gICAgZm9yIChsZXQgbmFtZSBvZiB0b1JlbW92ZSkge1xuICAgICAgICBub2RlLnN0eWxlLnJlbW92ZVByb3BlcnR5KG5hbWUpO1xuICAgIH1cbn07XG5cbmFsbG93ZWRUYWdzRXh0ZW5kZWRbXCJTUEFOXCJdID0gZmlsdGVyRXh0ZXJuYWxTcGFuO1xuXG4vLyBhZGQgYmFzaWMgdGFncyB0byBleHRlbmRlZFxuT2JqZWN0LmFzc2lnbihhbGxvd2VkVGFnc0V4dGVuZGVkLCBhbGxvd2VkVGFnc0Jhc2ljKTtcblxuLy8gZmlsdGVyaW5nIGZyb20gYW5vdGhlciBmaWVsZFxubGV0IGZpbHRlckludGVybmFsTm9kZSA9IGZ1bmN0aW9uIChub2RlKSB7XG4gICAgaWYgKG5vZGUuc3R5bGUpIHtcbiAgICAgICAgbm9kZS5zdHlsZS5yZW1vdmVQcm9wZXJ0eShcImJhY2tncm91bmQtY29sb3JcIik7XG4gICAgICAgIG5vZGUuc3R5bGUucmVtb3ZlUHJvcGVydHkoXCJmb250LXNpemVcIik7XG4gICAgICAgIG5vZGUuc3R5bGUucmVtb3ZlUHJvcGVydHkoXCJmb250LWZhbWlseVwiKTtcbiAgICB9XG4gICAgLy8gcmVjdXJzZVxuICAgIGZvciAoY29uc3QgY2hpbGQgb2Ygbm9kZS5jaGlsZE5vZGVzKSB7XG4gICAgICAgIGZpbHRlckludGVybmFsTm9kZShjaGlsZCk7XG4gICAgfVxufTtcblxuLy8gZmlsdGVyaW5nIGZyb20gZXh0ZXJuYWwgc291cmNlc1xubGV0IGZpbHRlck5vZGUgPSBmdW5jdGlvbiAobm9kZSwgZXh0ZW5kZWRNb2RlKSB7XG4gICAgLy8gdGV4dCBub2RlP1xuICAgIGlmIChub2RlLm5vZGVUeXBlID09PSAzKSB7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBkZXNjZW5kIGZpcnN0LCBhbmQgdGFrZSBhIGNvcHkgb2YgdGhlIGNoaWxkIG5vZGVzIGFzIHRoZSBsb29wIHdpbGwgc2tpcFxuICAgIC8vIGVsZW1lbnRzIGR1ZSB0byBub2RlIG1vZGlmaWNhdGlvbnMgb3RoZXJ3aXNlXG5cbiAgICBjb25zdCBub2RlcyA9IFtdO1xuICAgIGZvciAoY29uc3QgY2hpbGQgb2Ygbm9kZS5jaGlsZE5vZGVzKSB7XG4gICAgICAgIG5vZGVzLnB1c2goY2hpbGQpO1xuICAgIH1cbiAgICBmb3IgKGNvbnN0IGNoaWxkIG9mIG5vZGVzKSB7XG4gICAgICAgIGZpbHRlck5vZGUoY2hpbGQsIGV4dGVuZGVkTW9kZSk7XG4gICAgfVxuXG4gICAgaWYgKG5vZGUudGFnTmFtZSA9PT0gXCJBTktJVE9QXCIpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGxldCB0YWc7XG4gICAgaWYgKGV4dGVuZGVkTW9kZSkge1xuICAgICAgICB0YWcgPSBhbGxvd2VkVGFnc0V4dGVuZGVkW25vZGUudGFnTmFtZV07XG4gICAgfSBlbHNlIHtcbiAgICAgICAgdGFnID0gYWxsb3dlZFRhZ3NCYXNpY1tub2RlLnRhZ05hbWVdO1xuICAgIH1cbiAgICBpZiAoIXRhZykge1xuICAgICAgICBpZiAoIW5vZGUuaW5uZXJIVE1MIHx8IG5vZGUudGFnTmFtZSA9PT0gXCJUSVRMRVwiKSB7XG4gICAgICAgICAgICBub2RlLnBhcmVudE5vZGUucmVtb3ZlQ2hpbGQobm9kZSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBub2RlLm91dGVySFRNTCA9IG5vZGUuaW5uZXJIVE1MO1xuICAgICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgICAgaWYgKHR5cGVvZiB0YWcgPT09IFwiZnVuY3Rpb25cIikge1xuICAgICAgICAgICAgLy8gZmlsdGVyaW5nIGZ1bmN0aW9uIHByb3ZpZGVkXG4gICAgICAgICAgICB0YWcobm9kZSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBhbGxvd2VkLCBmaWx0ZXIgb3V0IGF0dHJpYnV0ZXNcbiAgICAgICAgICAgIGNvbnN0IHRvUmVtb3ZlID0gW107XG4gICAgICAgICAgICBmb3IgKGNvbnN0IGF0dHIgb2Ygbm9kZS5hdHRyaWJ1dGVzKSB7XG4gICAgICAgICAgICAgICAgY29uc3QgYXR0ck5hbWUgPSBhdHRyLm5hbWUudG9VcHBlckNhc2UoKTtcbiAgICAgICAgICAgICAgICBpZiAodGFnLmF0dHJzLmluZGV4T2YoYXR0ck5hbWUpID09PSAtMSkge1xuICAgICAgICAgICAgICAgICAgICB0b1JlbW92ZS5wdXNoKGF0dHIpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGZvciAoY29uc3QgYXR0cmlidXRlVG9SZW1vdmUgb2YgdG9SZW1vdmUpIHtcbiAgICAgICAgICAgICAgICBub2RlLnJlbW92ZUF0dHJpYnV0ZU5vZGUoYXR0cmlidXRlVG9SZW1vdmUpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxufTtcblxubGV0IGFkanVzdEZpZWxkc1RvcE1hcmdpbiA9IGZ1bmN0aW9uICgpIHtcbiAgICBjb25zdCB0b3BIZWlnaHQgPSAkKFwiI3RvcGJ1dHNcIikuaGVpZ2h0KCk7XG4gICAgY29uc3QgbWFyZ2luID0gdG9wSGVpZ2h0ICsgODtcbiAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChcImZpZWxkc1wiKS5zdHlsZS5tYXJnaW5Ub3AgPSBtYXJnaW4gKyBcInB4XCI7XG59O1xuXG5sZXQgbW91c2VEb3duID0gMDtcblxuJChmdW5jdGlvbiAoKSB7XG4gICAgZG9jdW1lbnQuYm9keS5vbm1vdXNlZG93biA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgbW91c2VEb3duKys7XG4gICAgfTtcblxuICAgIGRvY3VtZW50LmJvZHkub25tb3VzZXVwID0gZnVuY3Rpb24gKCkge1xuICAgICAgICBtb3VzZURvd24tLTtcbiAgICB9O1xuXG4gICAgZG9jdW1lbnQub25jbGljayA9IGZ1bmN0aW9uIChldnQ6IE1vdXNlRXZlbnQpIHtcbiAgICAgICAgY29uc3Qgc3JjID0gZXZ0LnRhcmdldCBhcyBFbGVtZW50O1xuICAgICAgICBpZiAoc3JjLnRhZ05hbWUgPT09IFwiSU1HXCIpIHtcbiAgICAgICAgICAgIC8vIGltYWdlIGNsaWNrZWQ7IGZpbmQgY29udGVudGVkaXRhYmxlIHBhcmVudFxuICAgICAgICAgICAgbGV0IHAgPSBzcmM7XG4gICAgICAgICAgICB3aGlsZSAoKHAgPSBwLnBhcmVudE5vZGUgYXMgRWxlbWVudCkpIHtcbiAgICAgICAgICAgICAgICBpZiAocC5jbGFzc05hbWUgPT09IFwiZmllbGRcIikge1xuICAgICAgICAgICAgICAgICAgICAkKFwiI1wiICsgcC5pZCkuZm9jdXMoKTtcbiAgICAgICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfTtcblxuICAgIC8vIHByZXZlbnQgZWRpdG9yIGJ1dHRvbnMgZnJvbSB0YWtpbmcgZm9jdXNcbiAgICAkKFwiYnV0dG9uLmxpbmtiXCIpLm9uKFwibW91c2Vkb3duXCIsIGZ1bmN0aW9uIChlKSB7XG4gICAgICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgICB9KTtcblxuICAgIHdpbmRvdy5vbnJlc2l6ZSA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgYWRqdXN0RmllbGRzVG9wTWFyZ2luKCk7XG4gICAgfTtcblxuICAgIGFkanVzdEZpZWxkc1RvcE1hcmdpbigpO1xufSk7XG4iXX0=