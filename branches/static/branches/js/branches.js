function get_service_url() {
    return "/branches/v1/"
}

$("#office-tree").kendoTreeList({
    dataSource: {
        transport: {
            read: {
                url: get_service_url() + "offices/",
                contentType: "application/json",
                dataType: "json"
            },
            update: {
                url: function(item) {
                    return get_service_url() + "offices/" + item.id + "/"
                },
                contentType: "application/json",
                dataType: "json",
                type: "PUT",
            },
            destroy: {
                url: function (item) {
                    return get_service_url() + "offices/" + item.id + "/"
                },
                type: "DELETE"
            },
            create: {
                url: function (item) {
                    return get_service_url() + "offices/" + item.parentId + "/add_child/"
                },
                contentType: "application/json",
                dataType: "json",
                type: "POST"
            },
            parameterMap: function (options) {
                return JSON.stringify(options);
            }
        },
        schema: {
            model: {
                id: "id",
                parentId: "parentId",
                fields: {
                    parentId: {field: "parentId", type: "number", nullable: true},
                    name: { field: "name",  type: "string"},
                    height: { field: "height", type: "number"}
                },
                expanded: true
            }
        }
    },
    toolbar: ["save", "cancel", {name: "refresh", text: "Refresh"} ],
    height: 580,
    editable: {
        mode: "incell",
        move: true,
    },
    dataBound: function (e) {
        var items = e.sender.items();
        for (var i = 0; i < items.length; i++) {
            var dataItem = e.sender.dataItem(items[i]);
            var row = $(items[i]);
            if (dataItem.isNew()) {
                row.find("[data-command='createchild']").hide();
            }
            else {
                row.find("[data-command='createchild']").show();
            }
        }
    },
    columns: [
        { field: "id", title: "ID", template: "Office #: id #", editable: function () {return false;}},
        { field: "name", title: "Name" },
        { field: "height", title: "Height", editable: function () {return false;}},
        { command: [{name: "createchild", text: "Add child"},"destroy" ], width: 240 }

    ],
    resizable: true
});

