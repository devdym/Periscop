$(document).ready(function () {
  $("#birds_table_sn").DataTable({
    columnDefs: [
      { targets: [2, 3, 4], orderable: false },
      { className: "dt-center", targets: "_all" },
    ],
    paging: false,
    searching: false,
  });
});

$(document).ready(function () {
  $("#birds_table").DataTable({
    columnDefs: [
      { targets: [3, 6, 9, 12, 15, 18], visible: false },
      { targets: [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17], orderable: false },
      { className: "dt-center", targets: "_all" },
    ],
    info: false,
    paging: false,
    searching: false,
    scroller: false,

    rowCallback: function (row, data, index) {
      //str1
      if (data[2] < bankb && data[3] == "B") {
        $(row).find("td:eq(2)").css("color", "#FF652F");
      }
      if (data[3] == "A") {
        $(row).find("td:eq(1)").css("font-weight", "700");
      }
      if (data[3] == "B") {
        $(row).find("td:eq(2)").css("font-weight", "700");
      }
      // str2
      if (data[5] < bankb && data[6] == "B") {
        $(row).find("td:eq(4)").css("color", "#FF652F");
      }
      if (data[6] == "A") {
        $(row).find("td:eq(3)").css("font-weight", "700");
      }
      if (data[6] == "B") {
        $(row).find("td:eq(4)").css("font-weight", "700");
      }
      //str3
      if (data[8] < bankb && data[9] == "B") {
        $(row).find("td:eq(6)").css("color", "#FF652F");
      }
      if (data[9] == "A") {
        $(row).find("td:eq(5)").css("font-weight", "700");
      }
      if (data[9] == "B") {
        $(row).find("td:eq(6)").css("font-weight", "700");
      }
      //str4
      if (data[11] < bankb && data[12] == "B") {
        $(row).find("td:eq(8)").css("color", "#FF652F");
      }
      if (data[12] == "A") {
        $(row).find("td:eq(7)").css("font-weight", "700");
      }
      if (data[12] == "B") {
        $(row).find("td:eq(8)").css("font-weight", "700");
      }
      //str5
      if (data[14] < bankb && data[15] == "B") {
        $(row).find("td:eq(10)").css("color", "#FF652F");
      }
      if (data[15] == "A") {
        $(row).find("td:eq(9)").css("font-weight", "700");
      }
      if (data[15] == "B") {
        $(row).find("td:eq(10)").css("font-weight", "700");
      }
      //str6
      if (data[17] < bankb && data[18] == "B") {
        $(row).find("td:eq(12)").css("color", "#FF652F");
      }
      if (data[18] == "A") {
        $(row).find("td:eq(11)").css("font-weight", "700");
      }
      if (data[18] == "B") {
        $(row).find("td:eq(12)").css("font-weight", "700");
      }
    },
  });
});

$(document).ready(function () {
  $("#fins_table").DataTable({
    columnDefs: [
      { targets: [3, 6, 9, 12, 15, 18], visible: false },
      { targets: [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17], orderable: false },
      { className: "dt-center", targets: "_all" },
    ],
    info: false,
    paging: false,
    searching: false,
    rowCallback: function (row, data, index) {
      //str1
      // if (data[1] < banka) {
      //   $(row).find("td:eq(1)").css("color", "red");
      // }
      if (data[2] < bankb && data[3] == "B") {
        $(row).find("td:eq(2)").css("color", "#FF652F");
      }
      if (data[3] == "A") {
        $(row).find("td:eq(1)").css("font-weight", "bold");
      }
      if (data[3] == "B") {
        $(row).find("td:eq(2)").css("font-weight", "bold");
      }
      // str2
      // if (data[4] < banka) {
      //   $(row).find("td:eq(3)").css("color", "red");
      // }
      if (data[5] < bankb && data[6] == "B") {
        $(row).find("td:eq(4)").css("color", "#FF652F");
      }
      if (data[6] == "A") {
        $(row).find("td:eq(3)").css("font-weight", "bold");
      }
      if (data[6] == "B") {
        $(row).find("td:eq(4)").css("font-weight", "bold");
      }
      //str3
      // if (data[7] < banka) {
      //   $(row).find("td:eq(5)").css("color", "red");
      // }
      if (data[8] < bankb && data[9] == "B") {
        $(row).find("td:eq(6)").css("color", "#FF652F");
      }
      if (data[9] == "A") {
        $(row).find("td:eq(5)").css("font-weight", "bold");
      }
      if (data[9] == "B") {
        $(row).find("td:eq(6)").css("font-weight", "bold");
      }
      //str4
      // if (data[10] < banka) {
      //   $(row).find("td:eq(7)").css("color", "red");
      // }
      if (data[11] < bankb && data[12] == "B") {
        $(row).find("td:eq(8)").css("color", "#FF652F");
      }
      if (data[12] == "A") {
        $(row).find("td:eq(7)").css("font-weight", "bold");
      }
      if (data[12] == "B") {
        $(row).find("td:eq(8)").css("font-weight", "bold");
      }
      //str5
      // if (data[13] < banka) {
      //   $(row).find("td:eq(9)").css("color", "red");
      // }
      if (data[14] < bankb && data[15] == "B") {
        $(row).find("td:eq(10)").css("color", "#FF652F");
      }
      if (data[15] == "A") {
        $(row).find("td:eq(9)").css("font-weight", "bold");
      }
      if (data[15] == "B") {
        $(row).find("td:eq(10)").css("font-weight", "bold");
      }
      //str6
      // if (data[16] < banka) {
      //   $(row).find("td:eq(11)").css("color", "red");
      // }
      if (data[17] < bankb && data[18] == "B") {
        $(row).find("td:eq(12)").css("color", "#FF652F");
      }
      if (data[18] == "A") {
        $(row).find("td:eq(11)").css("font-weight", "bold");
      }
      if (data[18] == "B") {
        $(row).find("td:eq(12)").css("font-weight", "bold");
      }
    },
  });
});
$(document).ready(function () {
  $("#fins_table_sn").DataTable({
    columnDefs: [
      { targets: [2, 3, 4], orderable: false },
      { className: "dt-center", targets: "_all" },
    ],
    paging: false,
    searching: false,
  });
});

$(document).ready(function () {
  $("#acc_table").DataTable({
    paging: false,
    searching: false,
  });
});
