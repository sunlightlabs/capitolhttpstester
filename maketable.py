#!/usr/bin/env python
# this is terrible --timball@sunlightfoundation.com
# GNU GPL v2.0
# but you probably shouldn't use this code for anything, it's terrible.

from __future__ import print_function

emoji_chk = '<svg class="icon"><use xlink:href="#status-ok"/></svg>'
emoji_hrm = '<svg class="icon"><use xlink:href="#emoji-1"/></svg>'
emoji_sad = '<svg class="icon"><use xlink:href="#emoji-2"/></svg>'
emoji_bad = '<svg class="icon"><use xlink:href="#emoji-3"/></svg>'
emoji_lrt = '<svg class="icon"><use xlink:href="#status-alert"/></svg>'
emoji_exx = '<svg class="icon"><use xlink:href="#status-x"/></svg>'


SSL_OKAY_counter={str(x): 0 for x in range(0, 13)}
entity_counter={str(x): 0 for x in range(0, 13)}

grade_scale = {'A': {'emoji': emoji_chk, 'sum':0},
               'B': {'emoji': emoji_hrm, 'sum':0},
               'C': {'emoji': emoji_sad, 'sum':0},
               'D': {'emoji': emoji_bad, 'sum':0},
               'F': {'emoji': emoji_exx, 'sum':0},
               'X': {'emoji': emoji_lrt, 'sum':0}}

grade_summary = {0: {'grade': 'A', 'emoji': grade_scale['A']['emoji'], 'explanation': "OKAY Great Job!"},
                 1: {'grade': 'B', 'emoji': grade_scale['B']['emoji'], 'explanation': "SSL worked, page has insecure non-relative internal links"},
                 2: {'grade': 'B', 'emoji': grade_scale['B']['emoji'], 'explanation': "SSL worked, page has mixed content"},
                 3: {'grade': 'C', 'emoji': grade_scale['C']['emoji'], 'explanation': "SSL worked, but redirected to insecure homepage"},
                 4: {'grade': 'D', 'emoji': grade_scale['D']['emoji'], 'explanation': "Invalid cert, content okay"},
                 5: {'grade': 'D', 'emoji': grade_scale['D']['emoji'], 'explanation': "Invalid cert, page has mixed conent"},
                 6: {'grade': 'D', 'emoji': grade_scale['D']['emoji'], 'explanation': "Invalid cert, redirected to insecure homepage"},
                 7: {'grade': 'F', 'emoji': grade_scale['F']['emoji'], 'explanation': "Valid cert, but redirected to generic chamber homepage"},
                 8: {'grade': 'F', 'emoji': grade_scale['F']['emoji'], 'explanation': "Invalid cert, and redirected to generic chamber homepage"},
                 9: {'grade': 'F', 'emoji': grade_scale['F']['emoji'], 'explanation': "Valid cert, server returned error"},
                10: {'grade': 'F', 'emoji': grade_scale['F']['emoji'], 'explanation': "Invalid cert, server returned error"},
                11: {'grade': 'F', 'emoji': grade_scale['F']['emoji'], 'explanation': "Unable to make SSL connection"},
                12: {'grade': 'X', 'emoji': grade_scale['X']['emoji'], 'explanation': "Unobtainable and scary dragons"},
                }


class GradeCounter:
    def __init__(self):
        self.global_counter={str(x): 0 for x in range(0, len(grade_summary.keys()))}
        self.entity_counter={str(x): 0 for x in range(0, len(grade_summary.keys()))}
        self.entity_total=0
        self.global_total=0

    def reset_entity(self):
        self.entity_counter={str(x): 0 for x in range(0, len(grade_summary.keys()))}
        self.entity_total=0

    def inc(self, number):
        self.entity_counter[str(number)] += 1
        self.global_counter[str(number)] += 1
        self.entity_total += 1
        self.global_total += 1

    def ghetto_print(self):
        import pprint
        print (pprint.pforma(self.entity_counter))

    def global_ghetto_print(self):
        import pprint
        print (pprint.pformat(self.global_counter))

    def print_counter(self, global_counter, anchor_id, data, f):
        # printer a nice summary
        import copy
        if global_counter:
            counter = self.global_counter
            total = self.global_total
        else:
            counter = self.entity_counter
            total = self.entity_total

        scale = copy.deepcopy(grade_scale)

        if data['type'] != '':
            data['type'] = data['type'] + 's'

        # bin up grades
        for i in range(0, len(grade_summary.keys())):
            scale[grade_summary[i]['grade']]['sum'] += counter[str(i)]

        print (u'<div class="table-header"><h3 id="%s_card">Report Card for %s %s</h3></div><table><thead><tr><th>Grade</th><th>Emoji</th><th>Count</th><th>Percentage</th></tr></thead><tbody>' % (anchor_id, data['body'].title(), data['type'].title()), file=f)

        for grade in (sorted(scale.keys()[:-1])):
            print(u'<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s%%</td></tr>'
                    % (grade, scale[grade]['emoji'], scale[grade]['sum'], round(float(scale[grade]['sum'])/float(total) * 100, 1)), file=f)
        print (u'<tr><td>%s</td><td></td><td>%s</td><td>%s</td></tr>' % ("Total", total, "100%"), file=f)
        print (u'</tbody></table>', file=f)



def print_html_header(f):
    u"""
<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="UTF-8">
    <title>Congressional HTTPS Survey</title>

    <style>
        /* Normalize */
        html{font-family:sans-serif;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}body{margin:0}article,aside,details,figcaption,figure,footer,header,hgroup,main,menu,nav,section,summary{display:block}audio,canvas,progress,video{display:inline-block;vertical-align:baseline}audio:not([controls]){display:none;height:0}[hidden],template{display:none}a{background-color:transparent}a:active,a:hover{outline:0}abbr[title]{border-bottom:1px dotted}b,strong{font-weight:700}dfn{font-style:italic}h1{font-size:2em;margin:.67em 0}mark{background:#ff0;color:#000}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sup{top:-.5em}sub{bottom:-.25em}img{border:0}svg:not(:root){overflow:hidden}figure{margin:1em 40px}hr{box-sizing:content-box;height:0}pre{overflow:auto}code,kbd,pre,samp{font-family:monospace,monospace;font-size:1em}button,input,optgroup,select,textarea{color:inherit;font:inherit;margin:0}button{overflow:visible}button,select{text-transform:none}button,html input[type="button"],/* 1 */
        input[type="reset"],input[type="submit"]{-webkit-appearance:button;cursor:pointer}button[disabled],html input[disabled]{cursor:default}button::-moz-focus-inner,input::-moz-focus-inner{border:0;padding:0}input{line-height:normal}input[type="checkbox"],input[type="radio"]{box-sizing:border-box;padding:0}input[type="number"]::-webkit-inner-spin-button,input[type="number"]::-webkit-outer-spin-button{height:auto}input[type="search"]{-webkit-appearance:textfield;box-sizing:content-box}input[type="search"]::-webkit-search-cancel-button,input[type="search"]::-webkit-search-decoration{-webkit-appearance:none}fieldset{border:1px solid silver;margin:0 2px;padding:.35em .625em .75em}legend{border:0;padding:0}textarea{overflow:auto}optgroup{font-weight:700}table{border-collapse:collapse;border-spacing:0}td,th{padding:0}

        /* Body */
        body {
            background: #EFECE9;
            color: #413e3c;
            font-family: "Helvetica Neue", "Helvetica", "Arial", sans-serif;
            font-size: 12px;
            padding: 20px;
            position: relative;
        }

        /* Tables */
        table {
            margin: auto;
            display: block;
            clear: both;
            border-collapse: collapse;
            border-spacing: 0;
            width: 660px;
            table-layout: fixed;
        }
        thead tr {
            background-color: #E0DDDA;
            color: #635F5D;
            font-weight: bold;
            border-top: 1px solid #f0eded;
            border-bottom: 2px solid #D6D4D1;
        }

        tbody tr:nth-of-type(odd) {
            background-color: #f9f8f8;
        }
        tbody tr:nth-of-type(even) {
            background-color: #ffffff;
        }
        tbody tr {
            border-bottom: 1px solid #f0eded;
            border-top: 1px solid #f0eded;
        }
        tbody tr:hover {
            background: #f0eded;
            transition: background 300ms;
        }

        th, td {
            text-align: left;
            padding: 10px 5px;
            max-width: 100px;
        }

        th:first-child,
        td:first-child {
            padding-left: 10px;
        }
        th:last-child,
        td:last-child {
            padding-right: 10px;
        }

        .td-redirect {
            overflow: hidden;
            word-wrap: break-word;
        }

        .td-issues {
            min-width: 100px;
        }

        td:first-child {
            max-width: 100px;
        }

        /* Icons */
        .icon {
            width: 25px;
            height: 25px;
            fill: #999999;
        }

        /* Icon Colors */
        .emoji-1 {
            fill: #f6c917;
        }
        .emoji-2 {
            fill: #F39C12;
        }
        .emoji-3 {
            fill: #EF4836;
        }
        .status-ok {
            fill: #2ECC71;
        }
        .status-alert {
            fill: #EF4836;
        }
        .status-x {
            fill: #EF4836;
        }

        /* Type and other elements */

        h1 {
            font-weight: normal;
            font-size: 20px;
            color: #635F5D;
            margin: 0;
            margin-bottom: 10px;
        }

        h1 a {
            color: inherit;
            text-decoration: none;
            border: 0;
        }

        h1 a:hover {
            color: #444;
        }

        .timestamp {
            padding-top: 100px;
            color: #b0b0b0;
            position: absolute;
            left: 20px;
        }

        h2 {
            color: #635f5c;
            line-height: 22px;
            font-size: 18px;
            border-top: 1px dashed #D6D4D1;
            padding-top: 100px;
            margin-top: 80px;
        }

        h2:first-child {
            border-top: 0px;
            margin-top: 30px;
        }

        h2 span {
            font-weight: normal;
        }

        h3 {
            font-weight: normal;
            color: #635f5c;
            line-height: 22px;
            font-size: 18px;
            padding-top: 20px;
        }

        a {
          color: #2D9EA4;
          text-decoration: none;
          border-bottom: 1px dotted #2D9EA4;
        }

        hr {
            height: 0;
            border: none;
            border-top: 1px dashed #ccc;
            margin: 75px 0;
        }

        header {
            position: fixed;
            top: 0;
            width: 100%;
            background: #F5F3F2;
            border-bottom: 2px solid #ffffff;
            padding: 20px;
            margin: 0 -20px;
            z-index: 1;
        }

        .nav {
            list-style: none;
            padding-left: 0;
            margin: 0;
            color: #ccc;
            width: 75%;

        }
        .nav span {
            display: inline-block;
            margin-right: 10px;
            margin-bottom: 2px;
        }
        .nav span:last-child {
            margin-right: 0px;
        }

        span.green {
            color: #2ECC71;
        }
        span.red {
            color: #EF4836;
        }

        /* Sunlight Logo*/

        .logo {
            width: 100px;
            height: 30px;
            position: absolute;
            right: 60px;
            top: 30px;
        }

        .st0{fill:#E0B525;}
        .st1{fill:#4D5B5B;}
        .st2{fill:#959FA0;}
        .st3{fill:none;}
        .st4{fill:#E8EBED;}
        .st5{fill:#E4D66A;}
        .st6{fill:#FCD943;enable-background:new;}
        .st7{fill:#F7C420;enable-background:new;}
        .st8{fill:#E4C83D;}
        .st9{fill:#F9E673;enable-background:new;}
        .st10{fill:#D3B346;}


        .table-header {
            width: 660px;
            margin: auto;
        }

        /* Media Query */
        @media only screen and (max-width: 700px){

            body {
                padding: 20px 5px;
            }

            header {
                margin: 0 -5px;
            }

        }

    </style>
</head>


<body>

<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">

    <symbol id="emoji-1" viewBox="0 0 41.4 41.4">
        <path class="emoji-1" fill="#7A7D7D" d="M20.7,2.6c4.8,0,9.4,1.9,12.8,5.3c3.4,3.4,5.3,8,5.3,12.8s-1.9,9.4-5.3,12.8c-3.4,3.4-8,5.3-12.8,5.3 s-9.4-1.9-12.8-5.3c-3.4-3.4-5.3-8-5.3-12.8s1.9-9.4,5.3-12.8C11.3,4.5,15.9,2.6,20.7,2.6 M20.7,0C9.3,0,0,9.3,0,20.7 c0,11.4,9.3,20.7,20.7,20.7c11.4,0,20.7-9.3,20.7-20.7C41.4,9.3,32.1,0,20.7,0L20.7,0z M16.2,10.3c-1.1,0-1.9,1.7-1.9,3.9 s0.9,3.9,1.9,3.9s1.9-1.7,1.9-3.9S17.2,10.3,16.2,10.3z M25.2,10.3c-1.1,0-1.9,1.7-1.9,3.9s0.9,3.9,1.9,3.9s1.9-1.7,1.9-3.9 S26.3,10.3,25.2,10.3z M12.9,32.3c0.1,0,0.1,0,0.2,0l18.1-2.6c0.7-0.1,1.2-0.8,1.1-1.5c-0.1-0.7-0.8-1.2-1.5-1.1l-18.1,2.6 c-0.7,0.1-1.2,0.8-1.1,1.5C11.7,31.9,12.3,32.3,12.9,32.3L12.9,32.3z"></path>
    </symbol>

    <symbol id="emoji-2" viewBox="0 0 41.4 41.4">
        <path class="emoji-2" fill="#7A7D7D" d="M20.7,2.6c4.8,0,9.4,1.9,12.8,5.3c3.4,3.4,5.3,8,5.3,12.8s-1.9,9.4-5.3,12.8c-3.4,3.4-8,5.3-12.8,5.3 s-9.4-1.9-12.8-5.3c-3.4-3.4-5.3-8-5.3-12.8s1.9-9.4,5.3-12.8C11.3,4.5,15.9,2.6,20.7,2.6 M20.7,0C9.3,0,0,9.3,0,20.7 c0,11.4,9.3,20.7,20.7,20.7c11.4,0,20.7-9.3,20.7-20.7C41.4,9.3,32.1,0,20.7,0L20.7,0z M16.2,10.3c-1.1,0-1.9,1.7-1.9,3.9 s0.9,3.9,1.9,3.9s1.9-1.7,1.9-3.9S17.2,10.3,16.2,10.3z M25.2,10.3c-1.1,0-1.9,1.7-1.9,3.9s0.9,3.9,1.9,3.9s1.9-1.7,1.9-3.9 S26.3,10.3,25.2,10.3z M20.7,23.3c-4.6,0-8.8,2.7-10.6,6.9c-0.3,0.7,0,1.4,0.7,1.7c0.7,0.3,1.4,0,1.7-0.7c1.4-3.3,4.7-5.4,8.3-5.4 c3.6,0,6.8,2.1,8.3,5.4c0.3,0.7,1.1,0.9,1.7,0.7c0.7-0.3,0.9-1.1,0.7-1.7C29.5,26,25.3,23.3,20.7,23.3L20.7,23.3z"></path>
    </symbol>

    <symbol id="emoji-3" viewBox="0 0 41.4 41.4">
        <path class="emoji-3" fill="#7A7D7D" d="M20.7,2.6c4.8,0,9.4,1.9,12.8,5.3c3.4,3.4,5.3,8,5.3,12.8s-1.9,9.4-5.3,12.8c-3.4,3.4-8,5.3-12.8,5.3 s-9.4-1.9-12.8-5.3c-3.4-3.4-5.3-8-5.3-12.8s1.9-9.4,5.3-12.8C11.3,4.5,15.9,2.6,20.7,2.6 M20.7,0C9.3,0,0,9.3,0,20.7 c0,11.4,9.3,20.7,20.7,20.7c11.4,0,20.7-9.3,20.7-20.7C41.4,9.3,32.1,0,20.7,0L20.7,0z M20.7,23.3c-4.6,0-8.8,2.7-10.6,6.9 c-0.3,0.7,0,1.4,0.7,1.7c0.7,0.3,1.4,0,1.7-0.7c1.4-3.3,4.7-5.4,8.3-5.4c3.6,0,6.8,2.1,8.3,5.4c0.3,0.7,1.1,0.9,1.7,0.7 c0.7-0.3,0.9-1.1,0.7-1.7C29.5,26,25.3,23.3,20.7,23.3L20.7,23.3z"></path>
        <path class="emoji-3" fill="#7A7D7D" d="M17.2,16.5l-1.1-1.1l1.1-1.1c0.5-0.5,0.5-1.3,0-1.8c-0.5-0.5-1.3-0.5-1.8,0l-1.1,1.1l-1.1-1.1 c-0.5-0.5-1.3-0.5-1.8,0c-0.5,0.5-0.5,1.3,0,1.8l1.1,1.1l-1.1,1.1c-0.5,0.5-0.5,1.3,0,1.8c0.5,0.5,1.3,0.5,1.8,0l1.1-1.1l1.1,1.1 c0.5,0.5,1.3,0.5,1.8,0C17.7,17.8,17.7,17,17.2,16.5z"></path>
        <path class="emoji-3" fill="#7A7D7D" d="M30.6,16.5l-1.1-1.1l1.1-1.1c0.5-0.5,0.5-1.3,0-1.8c-0.5-0.5-1.3-0.5-1.8,0l-1.1,1.1l-1.1-1.1 c-0.5-0.5-1.3-0.5-1.8,0c-0.5,0.5-0.5,1.3,0,1.8l1.1,1.1l-1.1,1.1c-0.5,0.5-0.5,1.3,0,1.8c0.5,0.5,1.3,0.5,1.8,0l1.1-1.1l1.1,1.1 c0.5,0.5,1.3,0.5,1.8,0C31.1,17.8,31.1,17,30.6,16.5z"></path>
    </symbol>


    <symbol id="status-ok" viewBox="0 0 41.4 41.4">
        <path class="status-ok" fill="#7A7D7D" d="M20.7,2.6c4.8,0,9.4,1.9,12.8,5.3c3.4,3.4,5.3,8,5.3,12.8s-1.9,9.4-5.3,12.8c-3.4,3.4-8,5.3-12.8,5.3 s-9.4-1.9-12.8-5.3c-3.4-3.4-5.3-8-5.3-12.8s1.9-9.4,5.3-12.8C11.3,4.5,15.9,2.6,20.7,2.6 M20.7,0C9.3,0,0,9.3,0,20.7 s9.3,20.7,20.7,20.7s20.7-9.3,20.7-20.7S32.1,0,20.7,0L20.7,0z M18.1,29.7c0,0,0.1,0,0.1,0c0.7,0,1.4-0.4,1.9-1l10.3-12.9 c0.9-1.1,0.7-2.7-0.4-3.6c-1.1-0.9-2.7-0.7-3.6,0.4l-8.5,10.7l-3.1-3.1c-1-1-2.6-1-3.7,0c-1,1-1,2.6,0,3.7l5.2,5.2 C16.8,29.5,17.4,29.7,18.1,29.7L18.1,29.7z"></path>
    </symbol>


    <symbol id="status-alert" viewBox="0 0 41.4 41.4">
        <path class="status-alert" fill="#7A7D7D" d="M20.7,25.9c-1.4,0-2.6-1.2-2.6-2.6V10.3c0-1.4,1.2-2.6,2.6-2.6s2.6,1.2,2.6,2.6v12.9 C23.3,24.7,22.1,25.9,20.7,25.9L20.7,25.9z M20.7,2.6c-4.8,0-9.4,1.9-12.8,5.3c-3.4,3.4-5.3,8-5.3,12.8s1.9,9.4,5.3,12.8 s8,5.3,12.8,5.3s9.4-1.9,12.8-5.3c3.4-3.4,5.3-8,5.3-12.8s-1.9-9.4-5.3-12.8C30.1,4.5,25.5,2.6,20.7,2.6 M20.7,0 c11.4,0,20.7,9.3,20.7,20.7s-9.3,20.7-20.7,20.7S0,32.1,0,20.7S9.3,0,20.7,0L20.7,0z M20.7,33.6c1.4,0,2.6-1.2,2.6-2.6 s-1.2-2.6-2.6-2.6s-2.6,1.2-2.6,2.6S19.3,33.6,20.7,33.6z"></path>
    </symbol>

    <symbol id="status-x" viewBox="0 0 41.4 41.4">
        <path class="status-x" fill="#7A7D7D" d="M20.7,2.6c4.8,0,9.4,1.9,12.8,5.3c3.4,3.4,5.3,8,5.3,12.8s-1.9,9.4-5.3,12.8c-3.4,3.4-8,5.3-12.8,5.3 s-9.4-1.9-12.8-5.3c-3.4-3.4-5.3-8-5.3-12.8s1.9-9.4,5.3-12.8C11.3,4.5,15.9,2.6,20.7,2.6 M20.7,0C9.3,0,0,9.3,0,20.7 s9.3,20.7,20.7,20.7s20.7-9.3,20.7-20.7S32.1,0,20.7,0L20.7,0z M24.3,20.7l5.9-5.9c1-1,1-2.6,0-3.7c-1-1-2.6-1-3.7,0L20.7,17 l-5.9-5.9c-1-1-2.6-1-3.7,0c-1,1-1,2.6,0,3.7l5.9,5.9l-5.9,5.9c-1,1-1,2.6,0,3.7c0.5,0.5,1.2,0.8,1.8,0.8c0.7,0,1.3-0.3,1.8-0.8 l5.9-5.9l5.9,5.9c0.5,0.5,1.2,0.8,1.8,0.8c0.7,0,1.3-0.3,1.8-0.8c1-1,1-2.6,0-3.7L24.3,20.7z"></path>
    </symbol>

    <symbol id="sunlight-logo" viewBox="0 0 300 90.1">
        <path class="st0" d="M42,24.1c-4.5,0-8.9,1-12.9,2.7c0.1,3.1,0.8,6.3,2.2,9.2c2.7,6.1,7.7,10.7,13.9,13.1c2.8,1.1,5.8,1.6,8.8,1.6 c0.6,0,1.3,0,1.9-0.1c2.8-8.8,1-18-4.1-25.1C48.6,24.6,45.3,24.1,42,24.1z"/>
        <g>
            <path class="st1" d="M117.6,18.8h-5.3v-1.2c0-2.4-1-4.5-3.7-4.5c-2.9,0-3.6,2.3-3.6,4.8c0,2.9,0.3,3.9,3,4.9l4.1,1.6 c4.7,1.8,5.6,4.7,5.6,10.2c0,6.2-2.3,10.9-9.2,10.9c-5.2,0-9.1-3.8-9.1-8.8v-2h5.3v1.7c0,1.9,1,3.8,3.7,3.8c3.6,0,3.9-2.1,3.9-5.5 c0-4-0.5-4.6-3.1-5.6l-3.8-1.6c-4.6-1.9-5.8-4.9-5.8-9.5c0-5.6,3-10.2,9.1-10.2c5.3,0,8.9,4.3,8.9,8.4V18.8z"/>
            <path class="st1" d="M138.7,36.8c0,4.8-3.9,8.6-8.6,8.6c-4.7,0-8.6-3.8-8.6-8.6V8.1h5.3v28.2c0,2.6,1.4,3.9,3.3,3.9 c1.9,0,3.3-1.2,3.3-3.9V8.1h5.3V36.8z"/>
            <path class="st1" d="M143.5,8.1h5.1l8,22.3h0.1V8.1h5.3v37.1h-5l-8.1-22.3h-0.1v22.3h-5.3V8.1z"/>
            <path class="st1" d="M166.8,8.1h5.3v31.8h10.5v5.3h-15.8V8.1z"/>
            <path class="st1" d="M186.2,8.1h5.3v37.1h-5.3V8.1z"/>
            <path class="st1" d="M196.4,16.8c0-6,4.6-9.1,8.9-9.1c4.3,0,8.9,3,8.9,9.1v1.9h-5.3v-1.9c0-2.6-1.7-3.7-3.6-3.7 c-1.9,0-3.6,1.2-3.6,3.7v19.6c0,2.6,1.7,3.7,3.6,3.7c1.9,0,3.6-1.2,3.6-3.7v-7h-4.2v-4.7h9.5v11.7c0,6-4.6,9.1-8.9,9.1 c-4.3,0-8.9-3-8.9-9.1V16.8z"/>
            <path class="st1" d="M218.9,8.1h5.3V24h6.6V8.1h5.3v37.1h-5.3V28.7h-6.6v16.5h-5.3V8.1z"/>
            <path class="st1" d="M245.2,13.1H239v-5h17.6v5h-6.1v32.1h-5.3V13.1z"/>
        </g>
        <g>
            <path class="st2" d="M104.2,66.6h9.1v3.3h-9.1v15.8h-3.9V51.8h15v3.3h-11.1V66.6z"/>
            <path class="st2" d="M136.5,68.5c0,5.6-0.9,10.4-3,13.9c-2.4,3.9-5.8,3.9-7,3.9c-6.8,0-10.1-5.5-10.1-17.3c0-8.2,1.8-17.8,10-17.8 C134.2,51.2,136.5,58.9,136.5,68.5z M120.5,68.2c0,11.5,2.3,14.8,6,14.8c4.5,0,6-5.3,6-14.2c0-9.4-1.6-14.3-6-14.3 C122.4,54.5,120.5,58.9,120.5,68.2z"/>
            <path class="st2" d="M145.1,51.8v23.6c0,4.1,0.1,7.6,4.7,7.6c3.8,0,5-2,5-7.4V51.8h3.7v23.6c0,3.7,0,10.9-8.7,10.9 c-8.4,0-8.5-5.8-8.5-10.8V51.8H145.1z"/>
            <path class="st2" d="M164.3,51.8h4.6l10.7,26.5l-0.2-26.5h3.5v33.9h-3.8l-11.6-29l0.2,29h-3.5V51.8z"/>
            <path class="st2" d="M189.4,51.8h5.6c3.9,0,6.4,0.6,8.6,2.5c2.9,2.5,4.7,8.4,4.7,14.1c0,6.3-2.1,11.9-4.5,14.4 c-2.7,2.8-6.7,2.8-8.2,2.8h-6.1V51.8z M193.3,82.4h2.6c3.9,0,5.4-2.2,5.8-2.7c1.4-2,2.5-5.6,2.5-11c0-4.9-0.8-7.5-1.5-9.1 c-1.6-3.7-4.5-4.4-7.1-4.4h-2.4V82.4z"/>
            <path class="st2" d="M220.9,51.8l7.6,33.9h-4l-2.1-9.8h-7.6l-2.1,9.8h-3.7l7.8-33.9H220.9z M221.8,72.7l-3.1-16.9l-3.2,16.9H221.8z"/>
            <path class="st2" d="M233.2,55.1h-6.5v-3.3h17v3.3H237v30.6h-3.9V55.1z"/>
            <path class="st2" d="M246.6,51.8h3.9v33.9h-3.9V51.8z"/>
            <path class="st2" d="M275.8,68.5c0,5.6-0.9,10.4-3,13.9c-2.4,3.9-5.8,3.9-7,3.9c-6.8,0-10.1-5.5-10.1-17.3c0-8.2,1.8-17.8,10-17.8 C273.5,51.2,275.8,58.9,275.8,68.5z M259.8,68.2c0,11.5,2.3,14.8,6,14.8c4.5,0,6-5.3,6-14.2c0-9.4-1.6-14.3-6-14.3 C261.7,54.5,259.8,58.9,259.8,68.2z"/>
            <path class="st2" d="M281.2,51.8h4.6l10.7,26.5l-0.2-26.5h3.5v33.9H296l-11.6-29l0.2,29h-3.5V51.8z"/>
        </g>
        <path class="st3" d="M62.8,2.6C59.9,1.5,57,1,54,1c-8.9,0-17.1,4.8-21.5,12.4c2.3,0.3,4.7,0.8,6.9,1.7c5.4,2,9.8,5.5,13,9.8 c0.5,0.2,1,0.3,1.5,0.5c8.5,3.2,14.9,9.6,18.5,17.3c2.1-2.3,3.7-4.9,4.9-7.9C82.1,21.8,75.6,7.4,62.8,2.6z"/>
        <path class="st4" d="M72,44.3c-4.1,4-9.6,6.7-15.5,7.3c-0.1,0.3-0.2,0.6-0.3,0.9C52,63.7,41.1,71.2,29.1,71.2c-3.5,0-7-0.6-10.3-1.9 c-3.1-1.2-5.8-2.8-8.2-4.8c2.5,9.9,9.7,18.5,20,22.4c3.7,1.4,7.6,2.1,11.5,2.1c13.4,0,25.6-8.4,30.4-21C75.4,60.1,75.1,51.6,72,44.3 z"/>
        <path class="st5" d="M56.9,50.5c5.6-0.7,10.8-3.3,14.7-7.2c-3.4-7.6-9.7-13.9-18.1-17.1c-0.1,0-0.2-0.1-0.2-0.1 C57.9,33.1,59.5,42,56.9,50.5z"/>
        <path class="st6" d="M10.7,44.7c3.2-8.4,9.5-14.9,17.4-18.5c0-3.2,0.5-6.4,1.7-9.5c0.3-0.9,0.7-1.7,1.2-2.6c-0.6,0-1.3-0.1-1.9-0.1 C17.5,14,6.9,21.3,2.8,32.2c-4,10.5-1.2,22,6.2,29.6C8.1,56.2,8.6,50.4,10.7,44.7z"/>
        <path class="st7" d="M29.1,25.8c4-1.7,8.4-2.6,12.9-2.6c3,0,5.9,0.4,8.8,1.2c-3-3.7-7-6.6-11.7-8.4c-2.3-0.9-4.6-1.4-7-1.7 c-0.5,0.9-0.9,1.8-1.3,2.8C29.6,19.9,29.1,22.8,29.1,25.8z"/>
        <path class="st8" d="M19.1,68.5c3.2,1.2,6.6,1.8,10,1.8c11.6,0,22.2-7.3,26.3-18.2c0.1-0.2,0.1-0.3,0.2-0.5c-0.5,0-1,0.1-1.6,0.1 c-3.1,0-6.2-0.6-9.2-1.7c-6.5-2.4-11.6-7.3-14.4-13.6c-1.3-3-2.1-6.1-2.2-9.2c-7.5,3.5-13.5,9.8-16.5,17.8C9.4,51,9,57.2,10.2,63 C12.7,65.3,15.7,67.2,19.1,68.5z"/>
        <g>
            <path class="st3" d="M29.1,70.3c11.6,0,22.2-7.3,26.3-18.2c0.1-0.2,0.1-0.3,0.2-0.5c-0.5,0-1,0.1-1.6,0.1c-3.1,0-6.2-0.6-9.2-1.7 c-6.5-2.4-11.6-7.3-14.4-13.6c-1.3-3-2.1-6.1-2.2-9.2c-7.5,3.5-13.5,9.8-16.5,17.8C9.4,51,9,57.2,10.2,63c2.5,2.3,5.5,4.2,8.9,5.5 C22.3,69.7,25.7,70.3,29.1,70.3z"/>
            <path class="st3" d="M28.1,26.2c0-3.2,0.5-6.4,1.7-9.5c0.3-0.9,0.7-1.7,1.2-2.6c-0.6,0-1.3-0.1-1.9-0.1C17.5,14,6.9,21.3,2.8,32.2 c-4,10.5-1.2,22,6.2,29.6c-0.9-5.6-0.4-11.4,1.7-17.1C13.9,36.4,20.3,29.8,28.1,26.2z"/>
            <path class="st3" d="M56.6,51.5c-0.1,0.3-0.2,0.6-0.3,0.9C52,63.7,41.1,71.2,29.1,71.2c-3.5,0-7-0.6-10.3-1.9 c-3.1-1.2-5.8-2.8-8.2-4.8c2.5,9.9,9.7,18.5,20,22.4c3.7,1.4,7.6,2.1,11.5,2.1c13.4,0,25.6-8.4,30.4-21c3-8,2.7-16.5-0.4-23.9 C67.9,48.3,62.5,50.9,56.6,51.5z"/>
            <path class="st9" d="M62.8,2.6C59.9,1.5,57,1,54,1c-8.9,0-17.1,4.8-21.5,12.4c2.3,0.3,4.7,0.8,6.9,1.7c5.4,2,9.8,5.5,13,9.8 c0.5,0.2,1,0.3,1.5,0.5c8.5,3.2,14.9,9.6,18.5,17.3c2.1-2.3,3.7-4.9,4.9-7.9C82.1,21.8,75.6,7.4,62.8,2.6z"/>
            <path class="st10" d="M63.1,1.7C60.2,0.6,57.1,0,54,0c-9.4,0-18,5.2-22.5,13.2c-0.8-0.1-1.6-0.1-2.4-0.1c-12,0-22.9,7.5-27.2,18.8 c-4.3,11.4-1,23.8,7.4,31.6c2.3,10.8,9.8,20.2,20.9,24.4c3.8,1.5,7.8,2.2,11.9,2.2c13.8,0,26.4-8.7,31.3-21.6 c3.2-8.4,2.7-17.3-0.5-24.9c2.3-2.4,4.1-5.3,5.4-8.5C83.2,21.7,76.4,6.7,63.1,1.7z M55.9,50.7c-0.6,0-1.3,0.1-1.9,0.1 c-3,0-6-0.5-8.8-1.6c-6.2-2.4-11.1-7-13.9-13.1c-1.3-3-2.1-6.1-2.2-9.2c4-1.8,8.4-2.7,12.9-2.7c3.3,0,6.6,0.5,9.8,1.5 C56.9,32.6,58.6,41.9,55.9,50.7z M53.3,26.1c0.1,0,0.2,0.1,0.2,0.1c8.4,3.2,14.7,9.5,18.1,17.1c-3.9,4-9.1,6.6-14.7,7.2 C59.5,42,57.9,33.1,53.3,26.1z M42,23.1c-4.5,0-8.9,0.9-12.9,2.6c0-3,0.5-5.9,1.6-8.8c0.4-1,0.8-1.9,1.3-2.8c2.4,0.3,4.8,0.8,7,1.7 c4.7,1.8,8.7,4.8,11.7,8.4C47.9,23.5,45,23.1,42,23.1z M72.3,42.6c-3.5-7.7-10-14-18.5-17.3c-0.5-0.2-1-0.4-1.5-0.5 c-3.2-4.3-7.6-7.8-13-9.8c-2.2-0.8-4.5-1.4-6.9-1.7C36.9,5.8,45.1,1,54,1c3,0,6,0.5,8.8,1.6c12.8,4.9,19.3,19.3,14.4,32.1 C76.1,37.6,74.4,40.3,72.3,42.6z M9,61.8C1.6,54.2-1.2,42.8,2.8,32.2C6.9,21.3,17.5,14,29.1,14c0.6,0,1.3,0,1.9,0.1 c-0.4,0.8-0.8,1.7-1.2,2.6c-1.2,3.1-1.7,6.3-1.7,9.5c-7.8,3.6-14.2,10.2-17.4,18.5C8.6,50.4,8.1,56.2,9,61.8z M11.6,45.1 c3-8,9.1-14.3,16.5-17.8c0.2,3.1,0.9,6.2,2.2,9.2c2.8,6.3,7.9,11.1,14.4,13.6c3,1.1,6,1.7,9.2,1.7c0.5,0,1.1,0,1.6-0.1 c-0.1,0.2-0.1,0.3-0.2,0.5C51.2,63,40.7,70.3,29.1,70.3c-3.4,0-6.8-0.6-10-1.8c-3.4-1.3-6.4-3.2-8.9-5.5C9,57.2,9.4,51,11.6,45.1z M72.4,68.1c-4.8,12.5-17,21-30.4,21c-3.9,0-7.8-0.7-11.5-2.1c-10.3-3.9-17.4-12.5-20-22.4c2.4,2,5.2,3.6,8.2,4.8 c3.3,1.3,6.8,1.9,10.3,1.9c12,0,22.9-7.5,27.2-18.8c0.1-0.3,0.2-0.6,0.3-0.9c5.9-0.6,11.3-3.2,15.5-7.3 C75.1,51.6,75.4,60.1,72.4,68.1z"/>
        </g>
    </symbol>
</svg>

<header>
<a href="https://sunlightfoundation.com" target="_new"><svg class="logo"><use xlink:href="#sunlight-logo"></use></svg></a>
<h1><a href="https://sunlightfoundation.com/blog/2015/05/26/sunlight-analysis-reveals-only-15-of-congressional-websites-are-https-ready" target="_new">Congressional HTTPS Survey</a></h1>
<div class="nav">
    <span><a href="#senate_member">Senate Members</a></span>
    <span><a href="#house_member">House Members</a></span>
    <span><a href="#senate_committee">Senate Committees</a></span>
    <span><a href="#house_committee">House Committees</a></span>
    <span><a href="#leadership_office">Leadership Offices</a></span>
    <span><a href="#support_office">Congressional Support Offices</a></span>
    <span><a href="#joint_committee">Joint Committees</a></span>
    <span><a href="#error_summary">Overall Report Card</a></span>
</header>
    """
    import os, time

    stmp = time.ctime(os.path.getmtime(filename))
    stmp_str = '\n<div class="table-header timestamp">Last updated: <span>%s</span></div>' % (stmp)

    print (print_html_header.__doc__ + stmp_str, file=f)


def no_half_grades(grade):
    # like vanderbilt we don't believe in +/-
    grade = grade.replace('-', '')
    grade = grade.replace('+', '')
    grade = grade.replace('D', 'F') # D's are failures
    grade = grade.replace('E', 'F')
    return grade


def update_counter():
    global SSL_OKAY_counter, entity_counter
    for i in range(0, 13):
        SSL_OKAY_counter[str(i)] += entity_counter[str(i)]



def print_grade_explainer(f):
    # table explining the grades
    print(u'<div class="table-header"><h2 id="#grade_explanation">Grade Explanation</h2></div>', file=f)
    print(u'<table><thead><tr><th>Grade</th><th>Emoji</th><th>Reason</th></tr></thead><tbody>', file=f)
    last_grade='X'
    for i in range(0,12):
        if last_grade == grade_summary[i]['grade']:
            # don't print grade
            print(u'<tr><td></td><td>%s</td><td>%s</td></tr>' % (grade_summary[i]['emoji'], grade_summary[i]['explanation']), file=f)
        else:
            print(u'<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>' % (grade_summary[i]['grade'], grade_summary[i]['emoji'], grade_summary[i]['explanation']), file=f)
        last_grade=grade_summary[i]['grade']
    print(u'</tbody></table>', file=f)


def gen_name(name, url):
    return '<a href="%s" target="_new">%s</a>' % (url, name)


def calc_ssl_okay(data):
    # tests for states and returns an intervalue based on how bad things are
    # this might be better served in capitolhttpstester.py but here we are
    # this is the scoring mechanism for the survey
    import re
    from fnmatch import translate as xlate
    global entity_counter
    grade = 100 # everyone fails hard

    emoji = ''

    # doodling while getting regex right
    body_url = "http://www.%s.gov" % (data['body'])
    body_url_r = xlate(body_url + '*')
    https_url = data['url']
    http_url = https_url.replace("https://", 'http://')
    re_g  = xlate(http_url + '*')
    re_g = re_g.replace('www\.', '(www\.)?')

    # best case
    if (    data['hostname_match']
        and data['http status'] == 200
        and data['redirects'] == False
        and data['mixed content'] == False
        and data['non-rel links'] == False):
            grade = 0
    # valid cert non-rel http links
    elif (  data['hostname_match']
        and data['http status'] == 200
        and data['redirects'] == False
        and data['mixed content'] == False
        and data['non-rel links'] == True):
            grade = 1
    # valid cert mixed content
    elif (  data['hostname_match']
        and data['http status'] == 200
        and data['redirects'] == False
        and data['mixed content'] == True):
        # and data['non-rel links'] == False): # don't care if non-rel links
            grade = 2
    # valid cert enforced non-ssl redirect to member site
    elif (  data['hostname_match']
        and data['redirects'] == True
        and re.match(re_g, data['redirect_url'], re.I|re.DOTALL)):
            grade = 3
    # invalid cert enforced non-ssl redirect to member site
    elif (  data['hostname_match'] == False
        and data['redirects'] == True
        and re.match(re_g, data['redirect_url'], re.I|re.DOTALL)):
            grade = 6
    # valid cert hard fail to leg body website
    elif (  data['hostname_match']
        and data['redirects'] == True
        and re.match(body_url_r, data['redirect_url'], re.I|re.DOTALL)):
            grade = 7
    # invalid cert but SSL ready
    elif (  data['hostname_match'] == False
        and data['http status'] == 200
        and data['redirects'] == False
        and data['mixed content'] == False
        and data['non-rel links'] == False):
            grade = 4
    # invalid cert content fixable
    elif (  data['hostname_match'] == False
        and data['http status'] == 200
        and data['redirects'] == False):
            grade = 5
    # invalid cert hard fail to leg body website
    elif (  data['hostname_match'] == False
        and data['redirects'] == True
        and re.match(body_url_r, data['redirect_url'], re.I|re.DOTALL)):
            grade = 8
    # valid cert and 4XX or 5XX response
    elif (  data['hostname_match']
        and data['http status'] >= 400
        and data['redirects'] == False):
            grade = 9
    # invalid cert and 4XX or 5XX response
    elif (  data['hostname_match'] == False
        and data['http status'] >= 400
        and data['redirects'] == False):
            grade = 10
    # SSL FAIL
    elif (  'cipher' not in data ):
            grade = 11
    else:
        grade = 12 # mark of the beast

    counter.inc(grade)
    return (grade)


def gen_ssl_info(data):
    if 'cipher' not in data:
       data['SSL_ver'] = "SSL FAIL"
       data['cipher'] = ""
       data['bits'] = ""
       data['notAfter'] = "SSL FAIL"
    else:
       data['bits'] =  str(data['bits']) +'b'

    return '%s %s %s' % (data['SSL_ver'], data['cipher'], data['bits'])


def gen_redirect_detect(data):
    ret_str = '&nbsp;'
    if data['redirects']:
        ret_str = '<a href="%s">%s</a>' % (data['redirect_url'], data['redirect_url'])
    return ret_str


def print_html_footer(f):
    print(u'</body>\n</html>', file=f)


def print_table_head(data, f):
    print (u'<table>', file=f)
    print (u'<thead>', file=f)
    print (u'<tr>', file=f)
    print (u'<th>Name</th>', file=f)       # data['name'] + data['url']
    print (u'<th>Emoji</th>', file=f) # emoji column
    print (u'<th>Grade</th>', file=f)   # calculated CHECK (works 100% no issues), sad emoji (mixed content), confused emoji (invalid ssl but no mixed content), poop emoji (nothing works), bounce emoji (redirected away from https), skull&cross (4XX,5XX errors)
    #print (u'<th>SSL info</th>', file=f) # data['SSL_ver'] + data['cipher'] + data['bits']
    #print (u'<th>SSL expires</th>', file=f) # data['notAfter']
    print (u'<th>Valid SSL Cert</th>', file=f) # data['hostname_match']
    print (u'<th>HTTP status</th>', file=f) # data['http status']
    print (u'<th>Redirect to</th>', file=f) # data['redirects'] + data['redirect_url']
    print (u'<th>Mixed Content</th>', file=f) # data['mixed content']
    print (u'<th>Non-Relative Links</th>', file=f) # data['non-rel links']
    print (u'<th>Issues</th>', file=f) # data['SSL issues']
    print (u'</tr>', file=f)
    print (u'</thead>\n<tbody>', file=f)


def valid_cert(bool):
    ret = ''
    if bool:
        ret = "Valid"
    else:
        ret = "<span class='red'>Invalid</span>"
    return ret


def mixed_content(bool):
    ret = ''
    if bool:
        ret = "<span class='red'>Yes</span>"
    else:
        ret = "No"
    return ret


def non_rel_links(bool):
    ret = ''
    if bool:
        ret = "<span class='red'>Yes</span>"
    else:
        ret = "No"
    return ret


def print_table_row(data, f):
    print (u'<tr>', file=f)
    # Name
    if data['state_dist'] != None:
        print (u'<td>%s<br>(%s)</td>' % (gen_name(data['name'], data['url']), data['state_dist']), file=f)
    else:
        print (u'<td>%s</td>' % (gen_name(data['name'], data['url'])), file=f)
    # SSL OKAY
    grade = calc_ssl_okay(data)
    print (u'<td>%s</td><td><strong>%s</strong></td>' % (grade_summary[grade]['emoji'], grade_summary[grade]['grade']), file=f) # emoji and score
    # SSL info
    #print (u'<td>%s</td>' % (gen_ssl_info(data)), file=f)
    # SSL expires
    #print (u'<td>%s</td>' % (data['notAfter']), file=f)
    # SSL Hostname Match
    print (u'<td>%s</td>' % (valid_cert(data['hostname_match'])), file=f)
    # HTTP status
    print (u'<td>%s</td>' % (data['http status']), file=f)
    # Redirect Detected
    print (u'<td class="td-redirect">%s</td>' % (gen_redirect_detect(data)), file=f)
    # SSL Issues
    # Mixed Content
    print (u'<td>%s</td>' % (mixed_content(data['mixed content'])), file=f)
    # Non-Relative Links
    print (u'<td>%s</td>' % (non_rel_links(data['non-rel links'])), file=f)
    print (u'<td class="td-issues">%s</td>' % grade_summary[grade]['explanation'], file=f)
    print (u'</tr>', file=f)


def print_table_foot(data, f):
    print (u'</tbody>', file=f)
    print (u'</table>', file=f)
    print (u'</body>\n</html>', file=f)
    print (u'', file=f)


def print_table_title(data, f):
    header=u'<div class="table-header"><h2 id="%s_%s">%s %ss<span> (<a href="#%s_%s_card">view report card</a>)</span></h2></div>' % (data['body'], data['type'], data['body'].title(), data['type'].title(), data['body'], data['type'])
    print (header, file=f)


def print_table(data, f):
    headings={}
    headings['body'] = data[0]['body']
    headings['type'] = data[0]['type']
    if headings['type'] == 'support':
        headings['body'] = "support"
        headings['type'] = 'office'
    elif headings['type'] == 'leadership':
        headings['body'] = "leadership"
        headings['type'] = 'office'
    counter.reset_entity()

    print_table_title(headings, f)
    anchor_id = "%s_%s" % (headings['body'], headings['type'])
    print_table_head(data, f)
    while data:
        item = data.pop(0)
        print_table_row(item, f)
    print_table_foot(data, f)
    counter.print_counter(False, anchor_id, headings, f)

#----------------------------------------------------------
import sys
def main(argv):
    import pprint
    import json
    import io
    global filename

    if len(argv) == 1:
        filename = argv[0]
    else:
        filename = 'out.json'

    with open(filename) as file:
        j = json.load(file)

    if len(argv) > 1:
        f = io.open(argv[0], 'w', encoding='utf8')
    else:
        f = io.open("tester-results.html", 'w', encoding='utf8')

    senators = []       # senate members
    members = []        # house members
    senate_cmte = []    # senate committees
    house_cmte = []     # house committees
    joint_cmte = []     # joint committees
    leadership = []
    support_office = []

    # first sort out the json pile
    while j:
        item = j.pop(0)
        if   (item['body'] == "senate" and item['type'] == "member"):
            senators.append(item)
        elif (item['body'] == "house" and item['type'] == "member"):
            members.append(item)
        elif (item['body'] == "senate" and item['type'] == "committee"):
            senate_cmte.append(item)
        elif (item['body'] == "house" and item['type'] == "committee"):
            house_cmte.append(item)
        elif (item['body'] == "house" and item['type'] == "Minority committee"):
            house_cmte.append(item)
        elif (item['type'] == 'leadership'):
            leadership.append(item)
        elif (item['type'] == 'support'):
            support_office.append(item)
        elif item['body'] == "joint":
            joint_cmte.append(item)


    print_html_header(f)
    for entity in (senators, members, senate_cmte, house_cmte, joint_cmte, leadership, support_office):
        print_table(entity, f)
    print(u'<div class="table-header" id="error_summary"></div>', file=f)
    headings = {}
    headings['body'] = "Overall"
    headings['type'] = ''
    counter.print_counter(True, 'overall', headings, f)
    print_grade_explainer(f) # only needed this for the sidebar
    print_html_footer(f)


if __name__ == "__main__":
    filename = 'out.json'
    counter = GradeCounter()
    main(sys.argv[1:])
