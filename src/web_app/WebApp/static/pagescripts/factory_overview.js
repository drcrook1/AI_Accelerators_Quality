var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host;

function create_factory_overview_from_json(f_json){
    return {"factory_id" : f_json["factory_id"], "total_widgets" : f_json["total_widgets"], "total_anomalies" : f_json["total_anomalies"], 
            "perc_anomalies" : f_json["percent_anomalies"], "trend_anomalies" : f_json["anomaly_trend"] }
}

function get_factory_overview_data(vm){
    var url = baseUrl + overview_factories_endpoint;
    $.getJSON(url, function(data){
        data.forEach(x => {
            n_factory = create_factory_overview_from_json(x)
            vm.factory_overviews.unshift(n_factory)
        });
    });
}

function factory_overview_vm(){
    var self = this;
    self.factory_overviews = ko.observableArray([]);
}

factory_overview_vm = new factory_overview_vm();
ko.applyBindings(factory_overview_vm, document.getElementById("factories_overview"));

get_factory_overview_data(factory_overview_vm)