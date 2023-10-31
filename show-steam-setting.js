// ==UserScript==
// @name         修改成人内容筛选
// @version      0.1
// @description  成人内容偏好设置增补
// @author       Fuyn
// @match        https://store.steampowered.com/account/preferences/
// @grant        none
// ==/UserScript==

(function() {
    'use strict';


    const targetElements = document.querySelectorAll('.preference_row.account_setting_not_customer_facing');


    targetElements.forEach((element) => {

        element.classList.remove('account_setting_not_customer_facing');
        element.classList.add('preference_row');
    });
})();
