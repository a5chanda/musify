const VF = Vex.Flow;

var div = document.getElementById("boo")
var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

// Size our svg:
renderer.resize(500, 500);

// And get a drawing context:
var context = renderer.getContext();

// Create a stave at position 10, 40 of width 400 on the canvas.
var stave = new VF.Stave(10, 40, 400);

// Add a clef and time signature.
stave.addClef("treble").addTimeSignature("4/4");

// Connect it to the rendering context and draw!
stave.setContext(context).draw();

var vf = new VF.Factory({
  renderer: {elementId: 'boo', width: 500, height: 200}
});

var score = vf.EasyScore();
var system = vf.System();

var arr = ['A5', 'B5', 'C5'];
var notes = [];


for(var i = 0; i < arr.length; i++) {
	notes.push(new VF.StaveNote({clef: "treble", keys: [arr[i].charAt(0) + "/" + arr[i].charAt(1)], duration: "q"}));	
}


// Create a voice in 4/4 and add above notes
var voice = new VF.Voice({num_beats: 4,  beat_value: 4});
voice.addTickables(notes);

// Format and justify the notes to 400 pixels.
var formatter = new VF.Formatter().joinVoices([voice]).format([voice], 400);

// Render voice
voice.draw(context, stave);