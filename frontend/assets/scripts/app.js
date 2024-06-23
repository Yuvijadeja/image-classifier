Dropzone.autoDiscover = false;

function init() {
  let dz = new Dropzone("#dropzone", {
    url: "/",
    maxFiles: 1,
    addRemoveLinks: true,
    dictDefaultMessage: "Some Message",
    autoProcessQueue: false
  });

  dz.on("addedfile", function () {
    if (dz.files[1] != null) {
      dz.removeFile(dz.files[0]);
    }
  });

  dz.on("complete", function (file) {
    let imageData = file.dataURL;

    var url = "http://127.0.0.1:5000/classify-image";

    $.post(url, {
      image_data: file.dataURL
    }, function (data, status) {
      console.log(data);
      if (!data || data.length == 0) {
        $("#resultHolder").hide();
        $("#divClassTable").hide();
        $("#error").show();
        return;
      }

      let match = null;
      let bestScore = -1;
      for (let i = 0; i < data.length; ++i) {
        let maxScoreForThisClass = Math.max(...data[i].similarity);
        if (maxScoreForThisClass > bestScore) {
          match = data[i];
          bestScore = maxScoreForThisClass;
        }
      }
      if (match) {
        $("#error").hide();
        $("#resultHolder").show();
        $("#divClassTable").show();
        $("#resultHolder").html($(`[data-player="${match.name}"`).html());
        let celebrities = match.celebrities;
        for (let celebrity in celebrities) {
          let index = celebrities[celebrity];
          let proabilityScore = match.similarity[index];
          let elementName = "#score_" + celebrity;
          $(elementName).html(proabilityScore);
        }
      }
    });
  });

  $("#submitBtn").on('click', function (e) {
    dz.processQueue();
  });
}

$(document).ready(function () {
  $("#error").hide();
  $("#resultHolder").hide();
  $("#divClassTable").hide();
  init();
});