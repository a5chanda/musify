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
			const notesPerBar = 20 + 2 // Notes + 2
      var div = document.getElementById("sheet_music");
      var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

      var arr = JSON.parse(res).notes;
      
      
      var noteList = []; // list of edited notes
      
      for (var i = 0; i < arr.length; i++) { //setting up notelist
        noteList.push(new VF.StaveNote({
          clef: "treble",
          keys: [arr[i].charAt(0) + "/" + (parseInt(arr[i].charAt(1)) - 1)],
          duration: "q"
        }));
      }

      // Size our svg:
      renderer.resize(arr.length * scaleFactor, arr.length * 8); //size determines length/width of image

      // And get a drawing context:
      var context = renderer.getContext();

      //*********Staves Setup    
      var staves = []
      for(var i = 0; i < (arr.length/20); i++){
        	staves.push(new VF.Stave(10, 130 * i, 21 * scaleFactor));
          staves[i].addClef("treble").addTimeSignature("4/4");
        	staves[i].setContext(context).draw();       
      }
      
      
      

      // Connect it to the rendering context and draw!




      var vf = new VF.Factory({
        renderer: {
          elementId: 'sheet_music',
          width: (scaleFactor * arr.length),
          height: 200
        }
      });
			
      var count = 0;
      var staves_count = 0;
      // var voice;
      var voices = [];
      var temp = [];
      
 
      
      for(var i = 0; i < arr.length; i++) {
      	if(count < 20 && i != arr.length - 1) {
        	temp.push(noteList[i]);
          count++;
        }  
        else {
        	count = 0;
          voice = new VF.Voice({
        		num_beats: temp.length,           
        		beat_value: 4
      		});
          console.log(temp.length);
          
      		voice.addTickables(temp); //add the notes to the voice   - Render voice
        	var formatter = new VF.Formatter().joinVoices([voice]).format([voice], temp.length * scaleFactor); 
          voice.draw(context, staves[staves_count]); //output the notes
          temp = [];
     		 
        staves_count++;
        }    
      }



      
      
      
      
      
      
      
      
      
      
      

      
    });
  })
})



