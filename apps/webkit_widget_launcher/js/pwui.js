// -------------------------------------------------------------------------------
// MIT License
//
// Copyright (c) 2018 pxlc@github
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
// -------------------------------------------------------------------------------

var pwui = {};

pwui.getAncestorByClassTag = function( start_el, cls_tag )
{
    var matching_el = null;
    var el = start_el.parentElement;

    while ( el != null ) {
        var cls_str = el.getAttribute("class");
        if ( cls_str ) {
            var re = new RegExp( "\\b" + cls_tag + "\\b" );
            if ( cls_str.search( re ) != -1 ) {
                matching_el = el;
            }
        }
        el = el.parentElement;
    }
    return matching_el;
}

pwui.call_python = function( cmd, params )
{
    // function to make a call back into the PySide python app
    //
    var py_call_obj = { "cmd": cmd, "params": params };
    pyCentralWdg.call_from_js( JSON.stringify( py_call_obj ) );
}

pwui.handle_cmd = function( evt, cmd_js_obj )
{
    var el = evt.target;
    var top_el = pwui.getAncestorByClassTag( el, "Q_cmd_top" );

    var cmd_name = top_el.getAttribute('pwui_cmd');
    pwui.hide_cmd_panel( cmd_name );

    var input_div_el = top_el.querySelector(".Q_cmd_input");
    var params = {};

    var input_el_list = input_div_el.querySelectorAll("input");
    for (var c=0; c < input_el_list.length; c++) {
        var input_el = input_el_list[ c ];
        var input_type = input_el.getAttribute("type");
        var param_name = input_el.getAttribute("name");
        var param_value = input_el.value;

        if (input_type == "checkbox") {
            param_value = input_el.checked;
        }
        else if (input_type == "radio") {
            param_value = null;
            if (input_el.checked) {
                param_value = input_el.value; 
            }
        }
        else if (input_type == "number") {
            if (input_el.getAttribute("num_type") == "int") {
                param_value = parseInt( input_el.value, 10 );
            }
            else {
                param_value = Number( input_el.value );
            }
        }

        if (param_value != null) {
            params[ param_name ] = param_value;
        }
    }

    var select_el_list = input_div_el.querySelectorAll("select");
    for (var c=0; c < select_el_list.length; c++) {
        var select_el = select_el_list[c];
        var param_name = select_el.getAttribute("name");
        var param_value = select_el.value;

        if (param_value.indexOf("JSON{") == 0) {
            param_value = JSON.parse( param_value.substr(4) );
        }
        else if (param_value === "null") {
            param_value = null;
        }

        params[ param_name ] = param_value;
    }

    var is_check_okay = cmd_js_obj.check_params( top_el, params );

    if (is_check_okay) {
        pwui.call_python( cmd_name, params );
    } else {
        // TODO: message to user?
    }
}


pwui.cmd_panel_html_base64 = "";

pwui.go_to_cmd_panel = function( cmd_name )
{
    pwui.check_cmd_panel_created( cmd_name );
}

pwui.check_cmd_panel_created = function( cmd_name )
{
    var cmd_container_div = document.getElementById("app_cmd_container_div");

    var cmd_el = cmd_container_div.querySelector("div[pwui_cmd_name='" + cmd_name + "']");
    if (! cmd_el ) {
        // build from scratch
        pwui.call_python('op:create_cmd_panel_html',
                            {'cmd_name': cmd_name,
                             'js_html_base64_var': 'pwui.cmd_panel_html_base64',
                             'js_completion_callback': "pwui.decode_cmd_panel('" + cmd_name + "');"});
        return;
    }

    pwui.open_cmd_panel( cmd_name );
}


pwui.decode_cmd_panel = function( cmd_name )
{
    var decoded_html = atob( pwui.cmd_panel_html_base64 );
    var cmd_container_div = document.getElementById("app_cmd_container_div");

    cmd_container_div.innerHTML = cmd_container_div.innerHTML + "\n" + decoded_html;

    pwui.open_cmd_panel( cmd_name );
}


pwui.hide_cmd_panel = function( cmd_name )
{
    var cmd_wrapper_el = document.querySelector("div[pwui_cmd_name='" + cmd_name + "']");
    if( cmd_wrapper_el ) {
        cmd_wrapper_el.style.display = "none";
    }
}


pwui.open_cmd_panel = function( cmd_name )
{
    // Hide all other command panels
    var cmd_container_div = document.getElementById("app_cmd_container_div");
    var all_cmd_el_list = cmd_container_div.querySelectorAll("div[pwui_cmd_name]");

    for (var c=0; c < all_cmd_el_list.length; c++) {
        var el = all_cmd_el_list[c];
        el.style.display = "none";
    }

    var cmd_wrapper_el = cmd_container_div.querySelector("div[pwui_cmd_name='" + cmd_name + "']");
    if( cmd_wrapper_el ) {
        cmd_wrapper_el.style.display = "block";
    } else {
        alert("Command '" + cmd_name + "' not found - unable to open its panel.");
    }
}


pwui.popmsg_close = function()
{
    var popmsg_top_el = document.getElementById("id_popmsg_blocker");
    popmsg_top_el.style.display = "none";
}


pwui.popmsg_open = function( title_text, body_text, ion_icon_info, show_progress, btn_info_list )
{
    var popmsg_top_el = document.getElementById("id_popmsg_blocker");

    var title_icon_el = document.getElementById("id_popmsg_title_icon");
    var title_text_el = document.getElementById("id_popmsg_title_text");
    var text_el = document.getElementById("id_popmsg_text");
    var btn_container_el = document.getElementById("id_popmsg_btn_container");

    title_text_el.innerHTML = title_text;
    text_el.innerHTML = body_text;

    if( ! ion_icon_info ) {
        title_icon_el.style.display = "none";
        title_text_el.style.marginLeft = "0px";
    } else {
        title_icon_el.style.display = "block";
        title_icon_el.className = ion_icon_info.icon_name;
        if( "color_str" in ion_icon_info ) {
            title_icon_el.style.color = ion_icon_info.color_str;
        } else {
            title_icon_el.style.color = "rgb(210, 210, 210)";
        }
        title_text_el.style.marginLeft = "8px";
    }

    if( btn_info_list.length ) {
        for( var c=0; c < btn_info_list.length; c++ ) {
            var html_arr = [];
            var btn_info = btn_info_list[ c ];
            if( btn_info ) {
                var onclick_js = "";
                if( 'js_to_exec' in btn_info ) {
                    onclick_js = btn_info.js_to_exec;
                }
                html_arr.push(
                    '<div class="pwui_button" style="width: 80px;" onclick="' + onclick_js +
                    '">' + btn_info.label + '</div>');
            }
        }
        btn_container_el.innerHTML = html_arr.join('');
        btn_container_el.style.display = "block";
    } else {
        btn_container_el.style.display = "none";
        btn_container_el.innerHTML = "";
    }

    popmsg_top_el.style.display = "block";
}


pwui.popmsg_set_progress = function( percentage_0_to_1, progress_info_html )
{
    var percentage_str = "" + parseInt( 100.0 * percentage_0_to_1 + 0.5 ) + "%";
    var progress_el = document.getElementById("id_popmsg_progress");
    progress_el.style.width = percentage_str;

    var progress_info_el = document.getElementById("id_popmsg_progress_info");
    if( progress_info_html ) {
        progress_info_el.innerHTML = progress_info_html;
    }
}


pwui.popmsg_get_progress_percent = function()
{
    var progress_el = document.getElementById("id_popmsg_progress");
    var percent = parseInt( progress_el.style.width.replace("%",""), 10 );
    return ( parseFloat( "" + percent ) / 100.0 );
}


pwui.test_popmsg_open = function()
{
    var body_text = "Spicy jalapeno bacon ipsum dolor amet venison dolore enim laboris meatloaf flank. Nostrud ut fugiat sed shoulder shankle duis proident. Nisi prosciutto doner nostrud, jowl burgdoggen boudin exercitation jerky chuck. Excepteur culpa commodo, pork belly tongue pork chop velit voluptate.";

    var ion_icon_info = {
        'icon_name': 'ion-erlenmeyer-flask',
        'color_str': 'orange'
    };

    // var ion_icon_info = {};

    var show_progress = false;
    var btn_info_list = [
        {'label': 'OK', 'js_to_exec': 'pwui.popmsg_close();'},
        {'label': 'CANCEL', 'js_to_exec': 'pwui.popmsg_close();'},
    ];

    pwui.popmsg_open( "Something Wicked", body_text, ion_icon_info, show_progress, btn_info_list );

    var progress_el = document.getElementById("id_popmsg_progress");
    progress_el.style.width = "0%";

    setTimeout( pwui.test_update_progress, 500 );
}


pwui.test_update_progress = function()
{
    var percent_0_to_1 = pwui.popmsg_get_progress_percent()
    var percent_int = parseInt( percent_0_to_1 * 100.0 + 0.5 );
    percent_0_to_1 = percent_0_to_1 + 0.01;
    pwui.popmsg_set_progress( percent_0_to_1, "&nbsp;&nbsp;&nbsp;" + percent_int + " %" );

    if( percent_int < 100 ) {
        setTimeout( pwui.test_update_progress, 500 );
    }
}


