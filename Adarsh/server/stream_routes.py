# Taken from megadlbot_oss <https://github.com/eyaadh/megadlbot_oss/blob/master/mega/webserver/routes.py>
# Thanks to Eyaadh <https://github.com/eyaadh>

import re
import time
import math
import logging
import secrets
import mimetypes
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from Adarsh.bot import multi_clients, work_loads, StreamBot
from Adarsh.server.exceptions import FIleNotFound, InvalidHash
from Adarsh import StartTime, __version__
from ..utils.time_format import get_readable_time
from ..utils.custom_dl import ByteStreamer
from Adarsh.utils.render_template import render_page
from Adarsh.vars import Var


routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    html_content = """
    <html lang="en" >
  <head>
    <meta charset="UTF-8">
    <title>Trooporiginals</title>
    <link rel="icon" type="image/png" href="https://www.linkpicture.com/q/IMG_20230911_185814_299.jpg">
    <meta name="viewport"
      content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
    <!-- <link rel="stylesheet" href="./style.css"> -->
    <style>
      @import url("https://fonts.googleapis.com/css?family=Quicksand:400,500,700&subset=latin-ext");
      html {
        position: relative;
        overflow-x: hidden !important;
      }

      * {
        box-sizing: border-box;
      }

      body {
        font-family: "Quicksand", sans-serif;
        color: #324e63;
      }

      a, a:hover {
        text-decoration: none;
      }

      .icon {
        display: inline-block;
        width: 1em;
        height: 1em;
        stroke-width: 0;
        stroke: currentColor;
        fill: currentColor;
      }

      .wrapper {
        width: 100%;
        width: 100%;
        height: auto;
        min-height: 100vh;
        padding: 50px 20px;
        padding-top: 100px;
        display: flex;
        background-image: linear-gradient(-20deg, #ff2846 0%, #6944ff 100%);
        display: flex;
        background-image: linear-gradient(-20deg, #ff2846 0%, #6944ff 100%);
      }
      @media screen and (max-width: 768px) {
        .wrapper {
          height: auto;
          min-height: 100vh;
          padding-top: 100px;
        }
      }

      .profile-card {
        width: 100%;
        min-height: 460px;
        margin: auto;
        box-shadow: 0px 8px 60px -10px rgba(13, 28, 39, 0.6);
        background: #fff;
        border-radius: 12px;
        max-width: 700px;
        position: relative;
      }
      .profile-card.active .profile-card__cnt {
        filter: blur(6px);
      }
      .profile-card.active .profile-card-message,
      .profile-card.active .profile-card__overlay {
        opacity: 1;
        pointer-events: auto;
        transition-delay: 0.1s;
      }
      .profile-card.active .profile-card-form {
        transform: none;
        transition-delay: 0.1s;
      }
      .profile-card__img {
        width: 150px;
        height: 150px;
        margin-left: auto;
        margin-right: auto;
        transform: translateY(-50%);
        border-radius: 50%;
        overflow: hidden;
        position: relative;
        z-index: 4;
        box-shadow: 0px 5px 50px 0px #6c44fc, 0px 0px 0px 7px rgba(107, 74, 255, 0.5);
      }
      @media screen and (max-width: 576px) {
        .profile-card__img {
          width: 120px;
          height: 120px;
        }
      }
      .profile-card__img img {
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
      }
      .profile-card__cnt {
        margin-top: -35px;
        text-align: center;
        padding: 0 20px;
        padding-bottom: 40px;
        transition: all 0.3s;
      }
      .profile-card__name {
        font-weight: 700;
        font-size: 24px;
        color: #2f03de;
        margin-bottom: 15px;
      }
      .profile-card__txt {
        font-size: 18px;
        font-weight: 500;
        color: #324e63;
        margin-top: 30px;
        margin-bottom: 15px;
      }
      .profile-card__txt strong {
        font-weight: 700;
      }
      .profile-card-loc {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 18px;
        font-weight: 600;
      }
      .profile-card-loc__icon {
        display: inline-flex;
        font-size: 27px;
        margin-right: 10px;
      }
      .profile-card-inf {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        align-items: flex-start;
        margin-top: 35px;
      }
      .profile-card-inf__item {
        padding: 10px 35px;
        min-width: 150px;
      }
      @media screen and (max-width: 768px) {
        .profile-card-inf__item {
          padding: 10px 20px;
          min-width: 120px;
        }
      }
      .profile-card-inf__title {
        font-weight: 700;
        font-size: 27px;
        color: #324e63;
      }
      .profile-card-inf__txt {
        font-weight: 500;
        margin-top: 7px;
      }
      .profile-card-social {
        margin-top: 25px;
        margin-bottom: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
      }
      .profile-card-social__item {
        display: inline-flex;
        width: 55px;
        height: 55px;
        margin: 15px;
        border-radius: 50%;
        align-items: center;
        justify-content: center;
        color: #fff;
        background: #405de6;
        box-shadow: 0px 7px 30px rgba(43, 98, 169, 0.5);
        position: relative;
        font-size: 21px;
        flex-shrink: 0;
        transition: all 0.3s;
      }
      @media screen and (max-width: 768px) {
        .profile-card-social__item {
          width: 50px;
          height: 50px;
          margin: 10px;
        }
      }
      @media screen and (min-width: 768px) {
        .profile-card-social__item:hover {
          transform: scale(1.2);
        }
      }
      .profile-card-social__item.twitter {
        background: linear-gradient(45deg, #1da1f2, #0e71c8);
        box-shadow: 0px 4px 30px rgba(19, 127, 212, 0.7);
      }
      .profile-card-social__item.instagram {
        background: linear-gradient(45deg, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d);
        box-shadow: 0px 4px 30px rgba(120, 64, 190, 0.6);
      }
      .profile-card-social__item.telegram {
        background: linear-gradient(45deg, #1769ff, #213fca);
        box-shadow: 0px 4px 30px rgba(27, 86, 231, 0.7);
      }
      .profile-card-social__item.github {
        background: linear-gradient(45deg, #333333, #626b73);
        box-shadow: 0px 4px 30px rgba(63, 65, 67, 0.6);
      }
      .profile-card-social__item.codepen {
        background: linear-gradient(45deg, #324e63, #414447);
        box-shadow: 0px 4px 30px rgba(55, 75, 90, 0.6);
      }
      .profile-card-social__item.link {
        background: linear-gradient(45deg, #d5135a, #f05924);
        box-shadow: 0px 4px 30px rgba(223, 45, 70, 0.6);
      }
      .profile-card-social .icon-font {
        display: inline-flex;
      }
      .profile-card-ctr {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 40px;
      }
      @media screen and (max-width: 576px) {
        .profile-card-ctr {
          flex-wrap: wrap;
        }
      }
      .profile-card__button {
        background: none;
        border: none;
        font-family: "Quicksand", sans-serif;
        font-weight: 700;
        font-size: 19px;
        margin: 15px 35px;
        padding: 15px 40px;
        min-width: 201px;
        border-radius: 50px;
        min-height: 55px;
        color: #fff;
        cursor: pointer;
        backface-visibility: hidden;
        transition: all 0.3s;
      }
      @media screen and (max-width: 768px) {
        .profile-card__button {
          min-width: 170px;
          margin: 15px 25px;
        }
      }
      @media screen and (max-width: 576px) {
        .profile-card__button {
          min-width: inherit;
          margin: 0;
          margin-bottom: 16px;
          width: 100%;
          max-width: 300px;
        }
        .profile-card__button:last-child {
          margin-bottom: 0;
        }
      }
      .profile-card__button:focus {
        outline: none !important;
      }
      @media screen and (min-width: 768px) {
        .profile-card__button:hover {
          transform: translateY(-5px);
        }
      }
      .profile-card__button:first-child {
        margin-left: 0;
      }
      .profile-card__button:last-child {
        margin-right: 0;
      }
      .profile-card__button.button--blue {
        background: linear-gradient(45deg, #1da1f2, #0e71c8);
        box-shadow: 0px 4px 30px rgba(19, 127, 212, 0.4);
      }
      .profile-card__button.button--blue:hover {
        box-shadow: 0px 7px 30px rgba(19, 127, 212, 0.75);
      }
      .profile-card__button.button--orange {
        background: linear-gradient(45deg, #d5135a, #f05924);
        box-shadow: 0px 4px 30px rgba(223, 45, 70, 0.35);
      }
      .profile-card__button.button--orange:hover {
        box-shadow: 0px 7px 30px rgba(223, 45, 70, 0.75);
      }
      .profile-card__button.button--gray {
        box-shadow: none;
        background: #dcdcdc;
        color: #142029;
      }
      .profile-card-message {
        width: 100%;
        height: 100%;
        position: absolute;
        top: 0;
        left: 0;
        padding-top: 130px;
        padding-bottom: 100px;
        opacity: 0;
        pointer-events: none;
        transition: all 0.3s;
      }
      .profile-card-form {
        box-shadow: 0 4px 30px rgba(15, 22, 56, 0.35);
        max-width: 80%;
        margin-left: auto;
        margin-right: auto;
        height: 100%;
        background: #fff;
        border-radius: 10px;
        padding: 35px;
        transform: scale(0.8);
        position: relative;
        z-index: 3;
        transition: all 0.3s;
      }
      @media screen and (max-width: 768px) {
        .profile-card-form {
          max-width: 90%;
          height: auto;
        }
      }
      @media screen and (max-width: 576px) {
        .profile-card-form {
          padding: 20px;
        }
      }
      .profile-card-form__bottom {
        justify-content: space-between;
        display: flex;
      }
      @media screen and (max-width: 576px) {
        .profile-card-form__bottom {
          flex-wrap: wrap;
        }
      }
      .profile-card textarea {
        width: 100%;
        resize: none;
        height: 210px;
        margin-bottom: 20px;
        border: 2px solid #dcdcdc;
        border-radius: 10px;
        padding: 15px 20px;
        color: #324e63;
        font-weight: 500;
        font-family: "Quicksand", sans-serif;
        outline: none;
        transition: all 0.3s;
      }
      .profile-card textarea:focus {
        outline: none;
        border-color: #8a979e;
      }
      .profile-card__overlay {
        width: 100%;
        height: 100%;
        position: absolute;
        top: 0;
        left: 0;
        pointer-events: none;
        opacity: 0;
        background: rgba(22, 33, 72, 0.35);
        border-radius: 12px;
        transition: all 0.3s;
      }
    </style>
  </head>
  <body>
    <!-- partial:index.partial.html -->
    <div class="wrapper">
      <div class="profile-card js-profile-card">
        <div class="profile-card__img">
          <img src="https://www.linkpicture.com/q/IMG_20230911_185814_299.jpg" alt="profile card">
        </div>
        <div class="profile-card__cnt js-profile-cnt">
          <div class="profile-card__name"><b>Troop<i> Originals</i></b></div>
          <div class="profile-card__txt">This is the home of page of Troops Files Stream link</div>
          <div class="profile-card__txt">Get All Movies to Watch Online/Download</div>
        
          <div class="profile-card-social">
            
          
            <h2> Telegram Bot  - </h2>
            <a href="https://telegram.me/TroopFiless_Bot" class="profile-card-social__item telegram" target="_blank">
              <span class="icon-font">
                <svg class="icon">
                  <use xlink:href="#icon-telegram"></use>
                </svg>
              </span>
            </a>
          </div>
          <div class="profile-card-social">
            <h2> Our Website - </h2>
            <a href="https://www.Trooporiginals.site" class="profile-card-social__item link" target="_blank">
              <span class="icon-font">
                <svg class="icon">
                  <use xlink:href="#icon-link"></use>
                </svg>
              </span>
            </a>
          </div>
          <div class="profile-card-social">
            <h2> Updates Channel - </h2>
            <a href="https://Telegram.me/Trooporiginals" class="profile-card-social__item github" target="_blank">
              <span class="icon-font">
                <svg class="icon">
                  <use xlink:href="#icon-telegram"></use>
                </svg>
              </span>
            </a>
          </div>
          <div class="profile-card-social">
            <h2> Backup Channel - </h2>
            <a href="https://telegram.me/TrooporiginalsBackup" class="profile-card-social__item link" target="_blank">
              <span class="icon-font">
                <svg class="icon">
                  <use xlink:href="#icon-link"></use>
                </svg>
              </span>
            </a>
          </div>
        </div>
        <div class="profile-card-message js-message">
          <form class="profile-card-form">
            <div class="profile-card-form__container">
              <textarea placeholder="Say something..."></textarea>
            </div>
            <div class="profile-card-form__bottom">
              <button class="profile-card__button button--blue js-message-close">
              Send
              </button>
              <button class="profile-card__button button--gray js-message-close">
              Cancel
              </button>
            </div>
          </form>
          <div class="profile-card__overlay js-message-close"></div>
        </div>
      </div>
    </div>
    <svg hidden="hidden">
      <defs>
        <symbol id="icon-codepen" viewBox="0 0 32 32">
          <title>codepen</title>
          <path d="M31.872 10.912v-0.032c0-0.064 0-0.064 0-0.096v-0.064c0-0.064 0-0.064-0.064-0.096 0 0 0-0.064-0.064-0.064 0-0.064-0.064-0.064-0.064-0.096 0 0 0-0.064-0.064-0.064 0-0.064-0.064-0.064-0.064-0.096l-0.192-0.192v-0.064l-0.064-0.064-14.592-9.696c-0.448-0.32-1.056-0.32-1.536 0l-14.528 9.696-0.32 0.32c0 0-0.064 0.064-0.064 0.096 0 0 0 0.064-0.064 0.064 0 0.064-0.064 0.064-0.064 0.096 0 0 0 0.064-0.064 0.064 0 0.064 0 0.064-0.064 0.096v0.064c0 0.064 0 0.064 0 0.096v0.064c0 0.064 0 0.096 0 0.16v9.696c0 0.064 0 0.096 0 0.16v0.064c0 0.064 0 0.064 0 0.096v0.064c0 0.064 0 0.064 0.064 0.096 0 0 0 0.064 0.064 0.064 0 0.064 0.064 0.064 0.064 0.096 0 0 0 0.064 0.064 0.064 0 0.064 0.064 0.064 0.064 0.096l0.256 0.256 0.064 0.032 14.528 9.728c0.224 0.16 0.48 0.224 0.768 0.224s0.544-0.064 0.768-0.224l14.528-9.728 0.32-0.32c0 0 0.064-0.064 0.064-0.096 0 0 0-0.064 0.064-0.064 0-0.064 0.064-0.064 0.064-0.096 0 0 0-0.064 0.064-0.064 0-0.064 0-0.064 0.064-0.096v-0.032c0-0.064 0-0.064 0-0.096v-0.064c0-0.064 0-0.096 0-0.16v-9.664c0-0.064 0-0.096 0-0.224zM17.312 4l10.688 7.136-4.768 3.168-5.92-3.936v-6.368zM14.56 4v6.368l-5.92 3.968-4.768-3.168 10.688-7.168zM2.784 13.664l3.392 2.304-3.392 2.304c0 0 0-4.608 0-4.608zM14.56 28l-10.688-7.136 4.768-3.2 5.92 3.936v6.4zM15.936 19.2l-4.832-3.232 4.832-3.232 4.832 3.232-4.832 3.232zM17.312 28v-6.432l5.92-3.936 4.8 3.168-10.72 7.2zM29.12 18.272l-3.392-2.304 3.392-2.304v4.608z"></path>
        </symbol>
        <symbol id="icon-github" viewBox="0 0 32 32">
          <title>github</title>
          <path d="M16.192 0.512c-8.832 0-16 7.168-16 16 0 7.072 4.576 13.056 10.944 15.168 0.8 0.16 1.088-0.352 1.088-0.768 0-0.384 0-1.632-0.032-2.976-4.448 0.96-5.376-1.888-5.376-1.888-0.736-1.856-1.792-2.336-1.792-2.336-1.44-0.992 0.096-0.96 0.096-0.96 1.6 0.128 2.464 1.664 2.464 1.664 1.44 2.432 3.744 1.728 4.672 1.344 0.128-1.024 0.544-1.728 1.024-2.144-3.552-0.448-7.296-1.824-7.296-7.936 0-1.76 0.64-3.168 1.664-4.288-0.16-0.416-0.704-2.016 0.16-4.224 0 0 1.344-0.416 4.416 1.632 1.28-0.352 2.656-0.544 4-0.544s2.72 0.192 4 0.544c3.040-2.080 4.384-1.632 4.384-1.632 0.864 2.208 0.32 3.84 0.16 4.224 1.024 1.12 1.632 2.56 1.632 4.288 0 6.144-3.744 7.488-7.296 7.904 0.576 0.512 1.088 1.472 1.088 2.976 0 2.144-0.032 3.872-0.032 4.384 0 0.416 0.288 0.928 1.088 0.768 6.368-2.112 10.944-8.128 10.944-15.168 0-8.896-7.168-16.032-16-16.032z"></path>
          <path d="M6.24 23.488c-0.032 0.064-0.16 0.096-0.288 0.064-0.128-0.064-0.192-0.16-0.128-0.256 0.032-0.096 0.16-0.096 0.288-0.064 0.128 0.064 0.192 0.16 0.128 0.256v0z"></path>
          <path d="M6.912 24.192c-0.064 0.064-0.224 0.032-0.32-0.064s-0.128-0.256-0.032-0.32c0.064-0.064 0.224-0.032 0.32 0.064s0.096 0.256 0.032 0.32v0z"></path>
          <path d="M7.52 25.12c-0.096 0.064-0.256 0-0.352-0.128s-0.096-0.32 0-0.384c0.096-0.064 0.256 0 0.352 0.128 0.128 0.128 0.128 0.32 0 0.384v0z"></path>
          <path d="M8.384 26.016c-0.096 0.096-0.288 0.064-0.416-0.064s-0.192-0.32-0.096-0.416c0.096-0.096 0.288-0.064 0.416 0.064 0.16 0.128 0.192 0.32 0.096 0.416v0z"></path>
          <path d="M9.6 26.528c-0.032 0.128-0.224 0.192-0.384 0.128-0.192-0.064-0.288-0.192-0.256-0.32s0.224-0.192 0.416-0.128c0.128 0.032 0.256 0.192 0.224 0.32v0z"></path>
          <path d="M10.912 26.624c0 0.128-0.16 0.256-0.352 0.256s-0.352-0.096-0.352-0.224c0-0.128 0.16-0.256 0.352-0.256 0.192-0.032 0.352 0.096 0.352 0.224v0z"></path>
          <path d="M12.128 26.4c0.032 0.128-0.096 0.256-0.288 0.288s-0.352-0.032-0.384-0.16c-0.032-0.128 0.096-0.256 0.288-0.288s0.352 0.032 0.384 0.16v0z"></path>
        </symbol>
        <symbol id="icon-location" viewBox="0 0 32 32">
          <title>location</title>
          <path d="M16 31.68c-0.352 0-0.672-0.064-1.024-0.16-0.8-0.256-1.44-0.832-1.824-1.6l-6.784-13.632c-1.664-3.36-1.568-7.328 0.32-10.592 1.856-3.2 4.992-5.152 8.608-5.376h1.376c3.648 0.224 6.752 2.176 8.608 5.376 1.888 3.264 2.016 7.232 0.352 10.592l-6.816 13.664c-0.288 0.608-0.8 1.12-1.408 1.408-0.448 0.224-0.928 0.32-1.408 0.32zM15.392 2.368c-2.88 0.192-5.408 1.76-6.912 4.352-1.536 2.688-1.632 5.92-0.288 8.672l6.816 13.632c0.128 0.256 0.352 0.448 0.64 0.544s0.576 0.064 0.832-0.064c0.224-0.096 0.384-0.288 0.48-0.48l6.816-13.664c1.376-2.752 1.248-5.984-0.288-8.672-1.472-2.56-4-4.128-6.88-4.32h-1.216zM16 17.888c-3.264 0-5.92-2.656-5.92-5.92 0-3.232 2.656-5.888 5.92-5.888s5.92 2.656 5.92 5.92c0 3.264-2.656 5.888-5.92 5.888zM16 8.128c-2.144 0-3.872 1.728-3.872 3.872s1.728 3.872 3.872 3.872 3.872-1.728 3.872-3.872c0-2.144-1.76-3.872-3.872-3.872z"></path>
          <path d="M16 32c-0.384 0-0.736-0.064-1.12-0.192-0.864-0.288-1.568-0.928-1.984-1.728l-6.784-13.664c-1.728-3.456-1.6-7.52 0.352-10.912 1.888-3.264 5.088-5.28 8.832-5.504h1.376c3.744 0.224 6.976 2.24 8.864 5.536 1.952 3.36 2.080 7.424 0.352 10.912l-6.784 13.632c-0.32 0.672-0.896 1.216-1.568 1.568-0.48 0.224-0.992 0.352-1.536 0.352zM15.36 0.64h-0.064c-3.488 0.224-6.56 2.112-8.32 5.216-1.824 3.168-1.952 7.040-0.32 10.304l6.816 13.632c0.32 0.672 0.928 1.184 1.632 1.44s1.472 0.192 2.176-0.16c0.544-0.288 1.024-0.736 1.28-1.28l6.816-13.632c1.632-3.264 1.504-7.136-0.32-10.304-1.824-3.104-4.864-5.024-8.384-5.216h-1.312zM16 29.952c-0.16 0-0.32-0.032-0.448-0.064-0.352-0.128-0.64-0.384-0.8-0.704l-6.816-13.664c-1.408-2.848-1.312-6.176 0.288-8.96 1.536-2.656 4.16-4.32 7.168-4.512h1.216c3.040 0.192 5.632 1.824 7.2 4.512 1.6 2.752 1.696 6.112 0.288 8.96l-6.848 13.632c-0.128 0.288-0.352 0.512-0.64 0.64-0.192 0.096-0.384 0.16-0.608 0.16zM15.424 2.688c-2.784 0.192-5.216 1.696-6.656 4.192-1.504 2.592-1.6 5.696-0.256 8.352l6.816 13.632c0.096 0.192 0.256 0.32 0.448 0.384s0.416 0.064 0.608-0.032c0.16-0.064 0.288-0.192 0.352-0.352l6.816-13.664c1.312-2.656 1.216-5.792-0.288-8.352-1.472-2.464-3.904-4-6.688-4.16h-1.152zM16 18.208c-3.424 0-6.24-2.784-6.24-6.24 0-3.424 2.816-6.208 6.24-6.208s6.24 2.784 6.24 6.24c0 3.424-2.816 6.208-6.24 6.208zM16 6.4c-3.072 0-5.6 2.496-5.6 5.6 0 3.072 2.528 5.6 5.6 5.6s5.6-2.496 5.6-5.6c0-3.104-2.528-5.6-5.6-5.6zM16 16.16c-2.304 0-4.16-1.888-4.16-4.16s1.888-4.16 4.16-4.16c2.304 0 4.16 1.888 4.16 4.16s-1.856 4.16-4.16 4.16zM16 8.448c-1.952 0-3.552 1.6-3.552 3.552s1.6 3.552 3.552 3.552c1.952 0 3.552-1.6 3.552-3.552s-1.6-3.552-3.552-3.552z"></path>
        </symbol>
        <symbol id="icon-instagram" viewBox="0 0 32 32">
          <title>instagram</title>
          <path d="M16 2.881c4.275 0 4.781 0.019 6.462 0.094 1.563 0.069 2.406 0.331 2.969 0.55 0.744 0.288 1.281 0.638 1.837 1.194 0.563 0.563 0.906 1.094 1.2 1.838 0.219 0.563 0.481 1.412 0.55 2.969 0.075 1.688 0.094 2.194 0.094 6.463s-0.019 4.781-0.094 6.463c-0.069 1.563-0.331 2.406-0.55 2.969-0.288 0.744-0.637 1.281-1.194 1.837-0.563 0.563-1.094 0.906-1.837 1.2-0.563 0.219-1.413 0.481-2.969 0.55-1.688 0.075-2.194 0.094-6.463 0.094s-4.781-0.019-6.463-0.094c-1.563-0.069-2.406-0.331-2.969-0.55-0.744-0.288-1.281-0.637-1.838-1.194-0.563-0.563-0.906-1.094-1.2-1.837-0.219-0.563-0.481-1.413-0.55-2.969-0.075-1.688-0.094-2.194-0.094-6.463s0.019-4.781 0.094-6.463c0.069-1.563 0.331-2.406 0.55-2.969 0.288-0.744 0.638-1.281 1.194-1.838 0.563-0.563 1.094-0.906 1.838-1.2 0.563-0.219 1.412-0.481 2.969-0.55 1.681-0.075 2.188-0.094 6.463-0.094zM16 0c-4.344 0-4.887 0.019-6.594 0.094-1.7 0.075-2.869 0.35-3.881 0.744-1.056 0.412-1.95 0.956-2.837 1.85-0.894 0.888-1.438 1.781-1.85 2.831-0.394 1.019-0.669 2.181-0.744 3.881-0.075 1.713-0.094 2.256-0.094 6.6s0.019 4.887 0.094 6.594c0.075 1.7 0.35 2.869 0.744 3.881 0.413 1.056 0.956 1.95 1.85 2.837 0.887 0.887 1.781 1.438 2.831 1.844 1.019 0.394 2.181 0.669 3.881 0.744 1.706 0.075 2.25 0.094 6.594 0.094s4.888-0.019 6.594-0.094c1.7-0.075 2.869-0.35 3.881-0.744 1.050-0.406 1.944-0.956 2.831-1.844s1.438-1.781 1.844-2.831c0.394-1.019 0.669-2.181 0.744-3.881 0.075-1.706 0.094-2.25 0.094-6.594s-0.019-4.887-0.094-6.594c-0.075-1.7-0.35-2.869-0.744-3.881-0.394-1.063-0.938-1.956-1.831-2.844-0.887-0.887-1.781-1.438-2.831-1.844-1.019-0.394-2.181-0.669-3.881-0.744-1.712-0.081-2.256-0.1-6.6-0.1v0z"></path>
          <path d="M16 7.781c-4.537 0-8.219 3.681-8.219 8.219s3.681 8.219 8.219 8.219 8.219-3.681 8.219-8.219c0-4.537-3.681-8.219-8.219-8.219zM16 21.331c-2.944 0-5.331-2.387-5.331-5.331s2.387-5.331 5.331-5.331c2.944 0 5.331 2.387 5.331 5.331s-2.387 5.331-5.331 5.331z"></path>
          <path d="M26.462 7.456c0 1.060-0.859 1.919-1.919 1.919s-1.919-0.859-1.919-1.919c0-1.060 0.859-1.919 1.919-1.919s1.919 0.859 1.919 1.919z"></path>
        </symbol>
        <symbol id="icon-twitter" viewBox="0 0 32 32">
          <title>twitter</title>
          <path d="M32 7.075c-1.175 0.525-2.444 0.875-3.769 1.031 1.356-0.813 2.394-2.1 2.887-3.631-1.269 0.75-2.675 1.3-4.169 1.594-1.2-1.275-2.906-2.069-4.794-2.069-3.625 0-6.563 2.938-6.563 6.563 0 0.512 0.056 1.012 0.169 1.494-5.456-0.275-10.294-2.888-13.531-6.862-0.563 0.969-0.887 2.1-0.887 3.3 0 2.275 1.156 4.287 2.919 5.463-1.075-0.031-2.087-0.331-2.975-0.819 0 0.025 0 0.056 0 0.081 0 3.181 2.263 5.838 5.269 6.437-0.55 0.15-1.131 0.231-1.731 0.231-0.425 0-0.831-0.044-1.237-0.119 0.838 2.606 3.263 4.506 6.131 4.563-2.25 1.762-5.075 2.813-8.156 2.813-0.531 0-1.050-0.031-1.569-0.094 2.913 1.869 6.362 2.95 10.069 2.95 12.075 0 18.681-10.006 18.681-18.681 0-0.287-0.006-0.569-0.019-0.85 1.281-0.919 2.394-2.075 3.275-3.394z"></path>
        </symbol>
        <symbol id="icon-telegram" viewBox="0 0 32 32">
          <title>telegram</title>
          <path d="M30.8,2.2L0.6,13.9c-0.8,0.3-0.7,1.3,0,1.6l7.4,2.8l2.9,9.2c0.2,0.6,0.9,0.8,1.4,0.4l4.1-3.4 c0.4-0.4,1-0.4,1.5,0l7.4,5.4c0.5,0.4,1.2,0.1,1.4-0.5L32,3.2C32.1,2.5,31.4,1.9,30.8,2.2z M25,8.3l-11.9,11 c-0.4,0.4-0.7,0.9-0.8,1.5l-0.4,3c-0.1,0.4-0.6,0.4-0.7,0.1l-1.6-5.5c-0.2-0.6,0.1-1.3,0.6-1.6l14.4-8.9C25,7.7,25.3,8.1,25,8.3z" />
        </symbol>
        <symbol id="icon-link" viewBox="0 0 32 32">
          <title>link</title>
          <path d="M17.984 11.456c-0.704 0.704-0.704 1.856 0 2.56 2.112 2.112 2.112 5.568 0 7.68l-5.12 5.12c-2.048 2.048-5.632 2.048-7.68 0-1.024-1.024-1.6-2.4-1.6-3.84s0.576-2.816 1.6-3.84c0.704-0.704 0.704-1.856 0-2.56s-1.856-0.704-2.56 0c-1.696 1.696-2.624 3.968-2.624 6.368 0 2.432 0.928 4.672 2.656 6.4 1.696 1.696 3.968 2.656 6.4 2.656s4.672-0.928 6.4-2.656l5.12-5.12c3.52-3.52 3.52-9.248 0-12.8-0.736-0.672-1.888-0.672-2.592 0.032z"></path>
          <path d="M29.344 2.656c-1.696-1.728-3.968-2.656-6.4-2.656s-4.672 0.928-6.4 2.656l-5.12 5.12c-3.52 3.52-3.52 9.248 0 12.8 0.352 0.352 0.8 0.544 1.28 0.544s0.928-0.192 1.28-0.544c0.704-0.704 0.704-1.856 0-2.56-2.112-2.112-2.112-5.568 0-7.68l5.12-5.12c2.048-2.048 5.632-2.048 7.68 0 1.024 1.024 1.6 2.4 1.6 3.84s-0.576 2.816-1.6 3.84c-0.704 0.704-0.704 1.856 0 2.56s1.856 0.704 2.56 0c1.696-1.696 2.656-3.968 2.656-6.4s-0.928-4.704-2.656-6.4z"></path>
        </symbol>
      </defs>
    </svg>
    <!-- partial -->
    <script>
      var messageBox = document.querySelector('.js-message');
      var btn = document.querySelector('.js-message-btn');
      var card = document.querySelector('.js-profile-card');
      var closeBtn = document.querySelectorAll('.js-message-close');

      btn.addEventListener('click',function (e) {
          e.preventDefault();
          card.classList.add('active');
      });

      closeBtn.forEach(function (element, index) {
        console.log(element);
          element.addEventListener('click',function (e) {
              e.preventDefault();
              card.classList.remove('active');
          });
      });
    </script>
  </body>
</html>
"""
    return web.Response(text=html_content, content_type='text/html')
        

@routes.get(r"/watch/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return web.Response(text=await render_page(id, secure_hash), content_type='text/html')
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))

@routes.get(r"/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return await media_streamer(request, id, secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))

class_cache = {}

async def media_streamer(request: web.Request, id: int, secure_hash: str):
    range_header = request.headers.get("Range", 0)
    
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    
    if Var.MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(id)
    logging.debug("after calling get_file_properties")
    
    if file_id.unique_id[:6] != secure_hash:
        logging.debug(f"Invalid hash for message with ID {id}")
        raise InvalidHash
    
    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = file_id.file_name
    disposition = "attachment"

    if mime_type:
        if not file_name:
            try:
                file_name = f"{secrets.token_hex(2)}.{mime_type.split('/')[1]}"
            except (IndexError, AttributeError):
                file_name = f"{secrets.token_hex(2)}.unknown"
    else:
        if file_name:
            mime_type = mimetypes.guess_type(file_id.file_name)
        else:
            mime_type = "application/octet-stream"
            file_name = f"{secrets.token_hex(2)}.unknown"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )
