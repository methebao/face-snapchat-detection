(function($) {
  function addEndpoint(isChecked) {
    if (isChecked) {
      $(".draw-links").each(function() {
        $(this).attr("href", $(this).attr("href") + "/1");
      });
    } else {
      $(".draw-links").each(function() {
        $(this).attr(
          "href",
          $(this)
            .attr("href")
            .replace("/1", "")
        );
      });
    }
  }
  if ($("#isRecording").is(":checked")) {
    addEndpoint(this.checked);
  }
  $("#isRecording").change(function() {
    addEndpoint(this.checked);
  });

  $(document).ready(function() {
    $("input:checkbox").prop("checked", false);

    var dir = "/videos";
    var fileextension = ".mp4";
    $.ajax({
      //This will retrieve the contents of the folder if the folder is configured as 'browsable'
      url: dir,
      success: function(data) {
        // List all mp4 file names in the page
        $(data)
          .find("a:contains(" + fileextension + ")")
          .each(function() {
            var filename = this.href
              .replace(window.location.host, "")
              .replace("http:///", "");
            $("body").append($("<img src=" + dir + filename + "></img>"));
          });
      }
    });
  });
})(jQuery);
