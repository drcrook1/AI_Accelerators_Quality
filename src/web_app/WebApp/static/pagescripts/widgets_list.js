var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host;

// function extract_line_json(l_json){
//     return {"line_id" : l_json["line_id"], "good_count" : l_json["good_count"], "bad_count" : l_json["bad_count"], 
//             "perc_anomalies" : l_json["perc_anomalies"], "anomaly_trend" : l_json["anomaly_trend"] }
// }

function get_widgets_list_data(vm){
    var url = baseUrl + fifty_widgets_endpoint;
    $.getJSON(url, function(data){
        data.forEach(x => {
            vm.widgets.unshift(JSON.parse(x));
        });
    });
}

function widgets_list_vm(){
    var self = this;
    self.widgets = ko.observableArray([]);
}

widgets_list_vm = new widgets_list_vm();
ko.applyBindings(widgets_list_vm, document.getElementById("widgets_list"));

get_widgets_list_data(widgets_list_vm);