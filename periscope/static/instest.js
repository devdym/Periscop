$(document).ready(function () {
  $("#test_table").DataTable({
    columnDefs: [
      {
        targets: [2, 3, 4, 5, 6, 7],
        orderable: false,
      },
    ],
    info: false,
    paging: false,

    rowCallback: function (row, data, index) {
      for (i = 2; i <= data.length; i++) {
        for (j = 0; j <= out_section.length; j++) {
          if (data[i] == out_section[j]) {
            $(row)
              .find("td:eq(" + i + ")")
              .css("color", "#FF652F");
          }
        }
      }
    },
  });
});
