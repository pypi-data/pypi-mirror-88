"use strict";
/* Copyright: Ankitects Pty Ltd and contributors
 * License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html */
var ankiPlatform = "desktop";
var typeans;
var _updatingQA = false;
var qFade = 100;
var aFade = 0;
var onUpdateHook;
var onShownHook;
function _runHook(arr) {
    var promises = [];
    for (var i = 0; i < arr.length; i++) {
        promises.push(arr[i]());
    }
    return Promise.all(promises);
}
function _updateQA(html, fadeTime, onupdate, onshown) {
    // if a request to update q/a comes in before the previous content
    // has been loaded, wait a while and try again
    if (_updatingQA) {
        setTimeout(function () {
            _updateQA(html, fadeTime, onupdate, onshown);
        }, 50);
        return;
    }
    _updatingQA = true;
    onUpdateHook = [onupdate];
    onShownHook = [onshown];
    var qa = $("#qa");
    // fade out current text
    new Promise((resolve) => qa.fadeOut(fadeTime, () => resolve()))
        // update text
        .then(() => {
        try {
            qa.html(html);
        }
        catch (err) {
            qa.html((`Invalid HTML on card: ${String(err).substring(0, 2000)}\n` +
                String(err.stack).substring(0, 2000)).replace(/\n/g, "<br />"));
        }
    })
        .then(() => _runHook(onUpdateHook))
        .then(() => 
    // @ts-ignore wait for mathjax to ready
    MathJax.startup.promise.then(() => {
        // @ts-ignore clear MathJax buffer
        MathJax.typesetClear();
        // @ts-ignore typeset
        return MathJax.typesetPromise(qa.slice(0, 1));
    }))
        // and reveal when processing is done
        .then(() => new Promise((resolve) => qa.fadeIn(fadeTime, () => resolve())))
        .then(() => _runHook(onShownHook))
        .then(() => (_updatingQA = false));
}
function _showQuestion(q, bodyclass) {
    _updateQA(q, qFade, function () {
        // return to top of window
        window.scrollTo(0, 0);
        document.body.className = bodyclass;
    }, function () {
        // focus typing area if visible
        typeans = document.getElementById("typeans");
        if (typeans) {
            typeans.focus();
        }
    });
}
function _showAnswer(a, bodyclass) {
    _updateQA(a, aFade, function () {
        if (bodyclass) {
            //  when previewing
            document.body.className = bodyclass;
        }
        // scroll to answer?
        var e = $("#answer");
        if (e[0]) {
            e[0].scrollIntoView();
        }
    }, function () { });
}
const _flagColours = {
    1: "#ff6666",
    2: "#ff9900",
    3: "#77ff77",
    4: "#77aaff",
};
function _drawFlag(flag) {
    var elem = $("#_flag");
    if (flag === 0) {
        elem.hide();
        return;
    }
    elem.show();
    elem.css("color", _flagColours[flag]);
}
function _drawMark(mark) {
    var elem = $("#_mark");
    if (!mark) {
        elem.hide();
    }
    else {
        elem.show();
    }
}
function _typeAnsPress() {
    if (window.event.keyCode === 13) {
        pycmd("ans");
    }
}
function _emulateMobile(enabled) {
    const list = document.documentElement.classList;
    if (enabled) {
        list.add("mobile");
    }
    else {
        list.remove("mobile");
    }
}
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmV2aWV3ZXIuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi8uLi8uLi8uLi8uLi8uLi8uLi8uLi9xdC9hcXQvZGF0YS93ZWIvanMvcmV2aWV3ZXIudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBO2tGQUNrRjtBQUVsRixJQUFJLFlBQVksR0FBRyxTQUFTLENBQUM7QUFDN0IsSUFBSSxPQUFPLENBQUM7QUFDWixJQUFJLFdBQVcsR0FBRyxLQUFLLENBQUM7QUFFeEIsSUFBSSxLQUFLLEdBQUcsR0FBRyxDQUFDO0FBQ2hCLElBQUksS0FBSyxHQUFHLENBQUMsQ0FBQztBQUVkLElBQUksWUFBWSxDQUFDO0FBQ2pCLElBQUksV0FBVyxDQUFDO0FBRWhCLFNBQVMsUUFBUSxDQUFDLEdBQXlCO0lBQ3ZDLElBQUksUUFBUSxHQUFHLEVBQUUsQ0FBQztJQUVsQixLQUFLLElBQUksQ0FBQyxHQUFHLENBQUMsRUFBRSxDQUFDLEdBQUcsR0FBRyxDQUFDLE1BQU0sRUFBRSxDQUFDLEVBQUUsRUFBRTtRQUNqQyxRQUFRLENBQUMsSUFBSSxDQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDLENBQUM7S0FDM0I7SUFFRCxPQUFPLE9BQU8sQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLENBQUM7QUFDakMsQ0FBQztBQUVELFNBQVMsU0FBUyxDQUFDLElBQUksRUFBRSxRQUFRLEVBQUUsUUFBUSxFQUFFLE9BQU87SUFDaEQsa0VBQWtFO0lBQ2xFLDhDQUE4QztJQUM5QyxJQUFJLFdBQVcsRUFBRTtRQUNiLFVBQVUsQ0FBQztZQUNQLFNBQVMsQ0FBQyxJQUFJLEVBQUUsUUFBUSxFQUFFLFFBQVEsRUFBRSxPQUFPLENBQUMsQ0FBQztRQUNqRCxDQUFDLEVBQUUsRUFBRSxDQUFDLENBQUM7UUFDUCxPQUFPO0tBQ1Y7SUFFRCxXQUFXLEdBQUcsSUFBSSxDQUFDO0lBRW5CLFlBQVksR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO0lBQzFCLFdBQVcsR0FB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dXJjZXNDb250ZW50IjpbIi8qIENvcHlyaWdodDogQW5raXRlY3RzIFB0eSBMdGQgYW5kIGNvbnRyaWJ1dG9yc1xuICogTGljZW5zZTogR05VIEFHUEwsIHZlcnNpb24gMyBvciBsYXRlcjsgaHR0cDovL3d3dy5nbnUub3JnL2xpY2Vuc2VzL2FncGwuaHRtbCAqL1xuXG52YXIgYW5raVBsYXRmb3JtID0gXCJkZXNrdG9wXCI7XG52YXIgdHlwZWFucztcbnZhciBfdXBkYXRpbmdRQSA9IGZhbHNlO1xuXG52YXIgcUZhZGUgPSAxMDA7XG52YXIgYUZhZGUgPSAwO1xuXG52YXIgb25VcGRhdGVIb29rO1xudmFyIG9uU2hvd25Ib29rO1xuXG5mdW5jdGlvbiBfcnVuSG9vayhhcnI6ICgpID0+IFByb21pc2U8YW55PltdKTogUHJvbWlzZTxhbnlbXT4ge1xuICAgIHZhciBwcm9taXNlcyA9IFtdO1xuXG4gICAgZm9yICh2YXIgaSA9IDA7IGkgPCBhcnIubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgcHJvbWlzZXMucHVzaChhcnJbaV0oKSk7XG4gICAgfVxuXG4gICAgcmV0dXJuIFByb21pc2UuYWxsKHByb21pc2VzKTtcbn1cblxuZnVuY3Rpb24gX3VwZGF0ZVFBKGh0bWwsIGZhZGVUaW1lLCBvbnVwZGF0ZSwgb25zaG93bikge1xuICAgIC8vIGlmIGEgcmVxdWVzdCB0byB1cGRhdGUgcS9hIGNvbWVzIGluIGJlZm9yZSB0aGUgcHJldmlvdXMgY29udGVudFxuICAgIC8vIGhhcyBiZWVuIGxvYWRlZCwgd2FpdCBhIHdoaWxlIGFuZCB0cnkgYWdhaW5cbiAgICBpZiAoX3VwZGF0aW5nUUEpIHtcbiAgICAgICAgc2V0VGltZW91dChmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgICBfdXBkYXRlUUEoaHRtbCwgZmFkZVRpbWUsIG9udXBkYXRlLCBvbnNob3duKTtcbiAgICAgICAgfSwgNTApO1xuICAgICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgX3VwZGF0aW5nUUEgPSB0cnVlO1xuXG4gICAgb25VcGRhdGVIb29rID0gW29udXBkYXRlXTtcbiAgICBvblNob3duSG9vayA9IFtvbnNob3duXTtcblxuICAgIHZhciBxYSA9ICQoXCIjcWFcIik7XG5cbiAgICAvLyBmYWRlIG91dCBjdXJyZW50IHRleHRcbiAgICBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4gcWEuZmFkZU91dChmYWRlVGltZSwgKCkgPT4gcmVzb2x2ZSgpKSlcbiAgICAgICAgLy8gdXBkYXRlIHRleHRcbiAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgICAgICBxYS5odG1sKGh0bWwpO1xuICAgICAgICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgICAgICAgICAgcWEuaHRtbChcbiAgICAgICAgICAgICAgICAgICAgKFxuICAgICAgICAgICAgICAgICAgICAgICAgYEludmFsaWQgSFRNTCBvbiBjYXJkOiAke1N0cmluZyhlcnIpLnN1YnN0cmluZygwLCAyMDAwKX1cXG5gICtcbiAgICAgICAgICAgICAgICAgICAgICAgIFN0cmluZyhlcnIuc3RhY2spLnN1YnN0cmluZygwLCAyMDAwKVxuICAgICAgICAgICAgICAgICAgICApLnJlcGxhY2UoL1xcbi9nLCBcIjxiciAvPlwiKVxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0pXG4gICAgICAgIC50aGVuKCgpID0+IF9ydW5Ib29rKG9uVXBkYXRlSG9vaykpXG4gICAgICAgIC50aGVuKCgpID0+XG4gICAgICAgICAgICAvLyBAdHMtaWdub3JlIHdhaXQgZm9yIG1hdGhqYXggdG8gcmVhZHlcbiAgICAgICAgICAgIE1hdGhKYXguc3RhcnR1cC5wcm9taXNlLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgIC8vIEB0cy1pZ25vcmUgY2xlYXIgTWF0aEpheCBidWZmZXJcbiAgICAgICAgICAgICAgICBNYXRoSmF4LnR5cGVzZXRDbGVhcigpO1xuXG4gICAgICAgICAgICAgICAgLy8gQHRzLWlnbm9yZSB0eXBlc2V0XG4gICAgICAgICAgICAgICAgcmV0dXJuIE1hdGhKYXgudHlwZXNldFByb21pc2UocWEuc2xpY2UoMCwgMSkpO1xuICAgICAgICAgICAgfSlcbiAgICAgICAgKVxuICAgICAgICAvLyBhbmQgcmV2ZWFsIHdoZW4gcHJvY2Vzc2luZyBpcyBkb25lXG4gICAgICAgIC50aGVuKCgpID0+IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiBxYS5mYWRlSW4oZmFkZVRpbWUsICgpID0+IHJlc29sdmUoKSkpKVxuICAgICAgICAudGhlbigoKSA9PiBfcnVuSG9vayhvblNob3duSG9vaykpXG4gICAgICAgIC50aGVuKCgpID0+IChfdXBkYXRpbmdRQSA9IGZhbHNlKSk7XG59XG5cbmZ1bmN0aW9uIF9zaG93UXVlc3Rpb24ocSwgYm9keWNsYXNzKSB7XG4gICAgX3VwZGF0ZVFBKFxuICAgICAgICBxLFxuICAgICAgICBxRmFkZSxcbiAgICAgICAgZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgLy8gcmV0dXJuIHRvIHRvcCBvZiB3aW5kb3dcbiAgICAgICAgICAgIHdpbmRvdy5zY3JvbGxUbygwLCAwKTtcblxuICAgICAgICAgICAgZG9jdW1lbnQuYm9keS5jbGFzc05hbWUgPSBib2R5Y2xhc3M7XG4gICAgICAgIH0sXG4gICAgICAgIGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIC8vIGZvY3VzIHR5cGluZyBhcmVhIGlmIHZpc2libGVcbiAgICAgICAgICAgIHR5cGVhbnMgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChcInR5cGVhbnNcIik7XG4gICAgICAgICAgICBpZiAodHlwZWFucykge1xuICAgICAgICAgICAgICAgIHR5cGVhbnMuZm9jdXMoKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICk7XG59XG5cbmZ1bmN0aW9uIF9zaG93QW5zd2VyKGEsIGJvZHljbGFzcykge1xuICAgIF91cGRhdGVRQShcbiAgICAgICAgYSxcbiAgICAgICAgYUZhZGUsXG4gICAgICAgIGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIGlmIChib2R5Y2xhc3MpIHtcbiAgICAgICAgICAgICAgICAvLyAgd2hlbiBwcmV2aWV3aW5nXG4gICAgICAgICAgICAgICAgZG9jdW1lbnQuYm9keS5jbGFzc05hbWUgPSBib2R5Y2xhc3M7XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICAgIC8vIHNjcm9sbCB0byBhbnN3ZXI/XG4gICAgICAgICAgICB2YXIgZSA9ICQoXCIjYW5zd2VyXCIpO1xuICAgICAgICAgICAgaWYgKGVbMF0pIHtcbiAgICAgICAgICAgICAgICBlWzBdLnNjcm9sbEludG9WaWV3KCk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGZ1bmN0aW9uICgpIHt9XG4gICAgKTtcbn1cblxuY29uc3QgX2ZsYWdDb2xvdXJzID0ge1xuICAgIDE6IFwiI2ZmNjY2NlwiLFxuICAgIDI6IFwiI2ZmOTkwMFwiLFxuICAgIDM6IFwiIzc3ZmY3N1wiLFxuICAgIDQ6IFwiIzc3YWFmZlwiLFxufTtcblxuZnVuY3Rpb24gX2RyYXdGbGFnKGZsYWcpIHtcbiAgICB2YXIgZWxlbSA9ICQoXCIjX2ZsYWdcIik7XG4gICAgaWYgKGZsYWcgPT09IDApIHtcbiAgICAgICAgZWxlbS5oaWRlKCk7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gICAgZWxlbS5zaG93KCk7XG4gICAgZWxlbS5jc3MoXCJjb2xvclwiLCBfZmxhZ0NvbG91cnNbZmxhZ10pO1xufVxuXG5mdW5jdGlvbiBfZHJhd01hcmsobWFyaykge1xuICAgIHZhciBlbGVtID0gJChcIiNfbWFya1wiKTtcbiAgICBpZiAoIW1hcmspIHtcbiAgICAgICAgZWxlbS5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgICAgZWxlbS5zaG93KCk7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBfdHlwZUFuc1ByZXNzKCkge1xuICAgIGlmICgod2luZG93LmV2ZW50IGFzIEtleWJvYXJkRXZlbnQpLmtleUNvZGUgPT09IDEzKSB7XG4gICAgICAgIHB5Y21kKFwiYW5zXCIpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gX2VtdWxhdGVNb2JpbGUoZW5hYmxlZDogYm9vbGVhbikge1xuICAgIGNvbnN0IGxpc3QgPSBkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQuY2xhc3NMaXN0O1xuICAgIGlmIChlbmFibGVkKSB7XG4gICAgICAgIGxpc3QuYWRkKFwibW9iaWxlXCIpO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIGxpc3QucmVtb3ZlKFwibW9iaWxlXCIpO1xuICAgIH1cbn1cbiJdfQ==