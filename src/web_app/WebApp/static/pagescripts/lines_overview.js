var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host;

function extract_line_json(l_json){
    return {"line_id" : l_json["line_id"], "good_count" : l_json["good_count"], "bad_count" : l_json["bad_count"], 
            "perc_anomalies" : l_json["perc_anomalies"], "anomaly_trend" : l_json["anomaly_trend"] }
}

function get_lines_overview_data(vm){
    var url = baseUrl + overview_lines_endpoint;
    $.getJSON(url, function(data){
        data.forEach(x => {
            x["line_overviews"].forEach(y => 
                {
                    l_overview = extract_line_json(y);
                    l_overview["factory_id"] = x["factory_id"];
                    vm.factories.unshift(l_overview);
                }); 
        });
    });
}

function lines_overview_vm(){
    var self = this;
    self.factories = ko.observableArray([]);
}

lines_overview_vm = new lines_overview_vm();
ko.applyBindings(lines_overview_vm, document.getElementById("lines_overview"));

get_lines_overview_data(lines_overview_vm);