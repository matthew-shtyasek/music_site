$(document).ready(function() {
  let play = true;
      $("#from_pause_to_play")[0].beginElement();
  $('#pause').on('click', function(event) {
    if(play) {
      play = false;
      $("#circle").attr("class", "");l
      $("#from_play_to_pause")[0].beginElement();
    } else {
      play = true;
      $("#circle").attr("class", "play");
      $("#from_pause_to_play")[0].beginElement();
    }
  });
});
