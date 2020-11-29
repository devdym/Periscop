$(document).ready(function () {
  $("#ballasting_table").DataTable({
    columnDefs: [
      { targets: "_all", orderable: false },
      { className: "dt-center", targets: "_all" },
    ],
    info: false,
    paging: false,
    searching: false,
    scroller: true,
    scrollY: 800,

    rowCallback: function (row, data, index) {
      for (i = 1; i <= data.length; i++) {
        if (data[i] < min_wa || data[i] > max_wa) {
          $(row)
            .find("td:eq(" + i + ")")
            .css("color", "#FF652F");
        }
      }
    },
  });
});
