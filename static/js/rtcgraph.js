/*
*  Graphing library for rtcscope.js
*  Copyright (c) 2015. All Rights Reserved.
*  Use of this source code is governed by a BSD-style license
*  that can be found in the LICENSE file in the root of the source
*  tree.
*/

Array.prototype.mapProperty = function(property) {
                        	return this.map(function (obj) {
                        	return obj[property];
                        	});
                		};

function getRandomColor() {
	var letters = '0123456789ABCDEF'.split('');
	var color = '#';
	for (var i = 0; i < 6; i++ ) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}

var label_time = [];
var id_set_map = {};

function gen_dataset(json_data, cid) {
	var dataset_member = {
                             label: cid,
			     fillColor : getRandomColor(),
              		     strokeColor : getRandomColor(),
                             pointColor : getRandomColor(),
                             pointStrokeColor : "#fff",
                             pointHighlightFill : "#fff",
                             pointHighlightStroke : "rgba(151,187,205,1)",
			     title : cid,
                             data : json_data.mapProperty('mean')
                             }
	return dataset_member;
}

function gen_label(json_data) {
	label_time = json_data.mapProperty('time')
	return label_time;
}

function get_data(graph_type) {
	var js_data = {};
	$.ajax({
	       url: "http://localhost:8000/v1/stats/?type=" + graph_type,
	       type: 'GET',
	       dataType: 'json',
	       async: false,
	       success: function (data, status) {
			js_data = data;
	                },
	       });
	return js_data;
}

function set_linechartdata(mydata) {
	var final_dataset = [];
	var final_label = [];
	var i = 0;
	for (var objct in mydata) {
		id_set_map[objct] = i;
		final_label = gen_label(mydata[objct]);
		final_dataset.push(gen_dataset(mydata[objct], objct));
		i++;
	}

	var chartdata = {
			labels : final_label,
			datasets : final_dataset
			}
	return chartdata;
}

function set_linechartdata_update(mydata) {
	var final_dataset = [];
        var final_label = [];

        for (var objct in mydata) {
        	final_label = gen_label(mydata[objct]);
                final_dataset.push(gen_dataset(mydata[objct], objct));

        }
        var chartdata = {
                        labels : final_label,
                        datasets : final_dataset
                        }
        return chartdata;
}

function update_linechartdata(graph_type) {
	var newChartDataJSON = {};
	var newData = get_data(graph_type);
	var newchartData = set_linechartdata_update(newData);
	newchartData["labels"] = (newchartData["labels"]).slice(Math.max((newchartData["labels"]).length - 3, 1));
	var keys = Object.keys(newData);
	for (i = 0; i < keys.length; i++) {
		newChartDataJSON[keys[i]] = {};
		newchartData["datasets"][i]["data"] = (newchartData["datasets"][i]["data"]).slice(Math.max((newchartData["datasets"][i]["data"]).length - 3, 1));
		for (j = 0; j < (newchartData["datasets"])[i]["data"].length; j++) {
			var obj = newChartDataJSON[keys[i]];
			var k = newchartData["labels"][j]
			var v = [(newchartData["datasets"][i]["data"][j])]
			obj[k] = v
		}
	}
	return newChartDataJSON;
}

function gen_dataset_member(cid) {

	var dataset_member = {
                             label: cid,
                             fillColor : getRandomColor(),
                             strokeColor : getRandomColor(),
                             pointColor : getRandomColor(),
                             pointStrokeColor : "#fff",
                             pointHighlightFill : "#fff",
                             pointHighlightStroke : "rgba(151,187,205,1)",
                             title : cid,
                             data : [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null]
                             }

	return dataset_member
}
