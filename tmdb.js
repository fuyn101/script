// ==UserScript==
// @name         tmdb辅助
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  一键复制名字为 " Indiana Jones and the Dial of Destiny (2023) [tmdbid=335977]"
// @author       Fuyn
// @match        https://www.themoviedb.org/
// @grant        none
// @updateURL    https://raw.githubusercontent.com/Fuynkio/js-script/main/tmdb.js
// ==/UserScript==


'use strict';
//季内 https://www.themoviedb.org/tv/75865/season/3

function copyTextToClipboard(text) {
    var tempTextArea = document.createElement('textarea');
    tempTextArea.value = text;
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    document.execCommand('copy');
    document.body.removeChild(tempTextArea);
}

function createCopyButtonWithCustomAction(locationSelector, buttonText, action) {
    var buttonLocation = document.querySelector(locationSelector);
    var copyButton = document.createElement('button');
    copyButton.textContent = buttonText;
    buttonLocation.appendChild(copyButton);

    copyButton.addEventListener('click', action);
}



var elements = document.querySelectorAll('div.episode_title h3');

// 对选定的元素进行操作
elements.forEach(function (element) {
    var episodeLink = element.querySelector('a.no_click.open');
    var Episode_message = episodeLink.getAttribute('title');
    Episode_message = Episode_message.replace(/:/g, '');
    var episodeElements = Episode_message.split(' ');
    var parts = episodeElements.slice(0, 7);
    var part8 = episodeElements.slice(7).join(' ');
    var combinedParts = `${parts[1]}${parts[2]}${parts[4]}${parts[5]} [${part8}] ${parts[3]}`;

    var button = document.createElement('button');
    button.textContent = '复制剧集';
    element.appendChild(button);
    button.addEventListener('click', function () {
        copyTextToClipboard(combinedParts)
    });
});

// 根据你提供的类名选择器，尝试找到适当的父元素
createCopyButtonWithCustomAction('ul.auto.actions', '复制数据', function () {
    // 从url中读取tmdb数字
    var tmdbid_Number = (window.location.href.match(/\/(\d+)(?:-|$)/) || [])[1];

    // 带年份的名字
    var tmdbid_year = ((document.querySelector('div.title.ott_true h2') || document.querySelector('div.title.ott_false h2')).textContent.match(/\((\d{4})\)\s*$/) || [])[1];

    var tmdbid_name_original = document.querySelector("p.wrap");
    tmdbid_name_original.textContent = tmdbid_name_original.textContent.replace(/原产地名称|原产地片名/g, ' ');

    var copy_tmdbid = `${tmdbid_name_original.textContent} (${tmdbid_year}) [tmdbid=${tmdbid_Number}]`;

    copy_tmdbid = copy_tmdbid.replace(/\s+/g, ' ');
    copyTextToClipboard(copy_tmdbid);
}
);


