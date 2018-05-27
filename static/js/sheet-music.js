$(document).ready(function() {
  $('#song').change(function(e) {
    var fileName = e.target.files[0].name;
    console.log(fileName);
    $.ajax({
      url: '/req',
      method: 'POST',
      data: {name: fileName}
    }).done(function(res) {
      console.log(res);
      console.log(JSON.parse(res).notes);
      $('#hide_on_load').css('display', 'none');

      const VF = Vex.Flow;
      const scaleFactor = 50
      var div = document.getElementById("sheet_music");
      var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

      var arr = JSON.parse(res).notes
      var noteList = []; // list of edited notes
    
      // Size our svg:
      renderer.resize(arr.length*scaleFactor, 200); //size determines length/width of image
    
      // And get a drawing context:
      var context = renderer.getContext();
    
      // Create a stave at position 10, 40 of width 800 on the canvas.
      var stave = new VF.Stave(10, 40, arr.length * scaleFactor); //last entry determines end of stave
    
      // Add a clef and time signature.
      stave.addClef("treble").addTimeSignature("4/4");
      //stave2.addClef("treble").addTimeSignature("4/4");
    
      // Connect it to the rendering context and draw!
      stave.setContext(context).draw();
    
      
      var vf = new VF.Factory({
        renderer: {elementId: 'sheet_music', width: (scaleFactor * arr.length), height: 200}
      });


      for(var i = 0; i < arr.length; i++) {
          noteList.push(new VF.StaveNote({clef: "treble", keys: [arr[i].charAt(0) + "/" + arr[i].charAt(1)], duration: "q"}));	
      }


      // Create a voice in 4/4 and add above notes
      var voice = new VF.Voice({num_beats: noteList.length,  beat_value: 4});
      voice.addTickables(noteList);

      // Format and justify the notes to 400 pixels.
      var formatter = new VF.Formatter().joinVoices([voice]).format([voice], noteList.length * scaleFactor);

      // Render voice
      voice.draw(context, stave);
      
    });
  })
})



