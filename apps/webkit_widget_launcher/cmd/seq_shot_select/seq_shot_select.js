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

var CMD_seq_shot_select = {};

CMD_seq_shot_select.check_params = function ( top_el )
{
    // return true if okay to continue to execute command, return false otherwise.
    console.log(":: got into CheckParams_shot_select() function!");
    return true;
}


CMD_seq_shot_select.shot_object_list = [];


CMD_seq_shot_select.rebuild_shot_select = function( shot_select_id )
{
    var shot_select_el = document.getElementById( shot_select_id );
    shot_select_el.innerHTML = "";

    var html = '<option value="null" disabled selected>Select Shot</option>\n';

    for (var c=0; c < CMD_seq_shot_select.shot_object_list.length; c++ ) {
        var shot = CMD_seq_shot_select.shot_object_list[c];
        html = html + '<option value=\'JSON{"id":' + shot.id + ',"code":"' + shot.code +
                '","entity_type":"Shot"}\'>' + shot.code + '</option>\n';
    }

    shot_select_el.innerHTML = html;
}


CMD_seq_shot_select.trigger_shot_select_rebuild = function( evt )
{
    var seq_select_el = evt.target;

    var seq = JSON.parse( seq_select_el.value.substr(4) );

    var top_el = pwui.getAncestorByClassTag( seq_select_el, "Q_cmd_top" );
    var shot_select_el = top_el.querySelector('SELECT[name="shot"]');

    var select_id = shot_select_el.getAttribute("id")

    CMD_seq_shot_select.shot_object_list = [];

    pwui.call_python( "op:rebuild_shot_select",
                        { "filler_info": {
                                "js_completion_stmt": "CMD_seq_shot_select.rebuild_shot_select('" + select_id + "');",
                                "target_js_list": "CMD_seq_shot_select.shot_object_list", "filler_type": "data_list",
                                "query_info": {"backend_server": "data/main_projects.db", "backend_type": "sqlite3",
                                                "entity_type": "Shot", "filters": [ ["sequence_id", "=", seq.id] ],
                                                "fields": ["id","code"], "order_by": ["id","asc"]}
                            } } )
}


