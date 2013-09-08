var canvas = document.getElementById("vexflow-canvas");
var renderer = new Vex.Flow.Renderer(canvas, Vex.Flow.Renderer.Backends.CANVAS);

var ctx = renderer.getContext();
var stave = new Vex.Flow.Stave(10, 60, 960);

// Add a treble clef
stave.addClef("treble");
stave.setContext(ctx).draw();

var notes = [
    // // Dotted eighth E##
    // new Vex.Flow.StaveNote({ keys: ["e##/5"], duration: "8d" }).
    //     addAccidental(0, new Vex.Flow.Accidental("##")).addDotToAll(),

    // // Sixteenth Eb
    // new Vex.Flow.StaveNote({ keys: ["eb/5"], duration: "16" }).
    //     addAccidental(0, new Vex.Flow.Accidental("b")),

    // // Half D
    // new Vex.Flow.StaveNote({ keys: ["d/5"], duration: "h" }),

    // // Quarter Cm#5
    // new Vex.Flow.StaveNote({ keys: ["c/5", "eb/5", "g#/5"], duration: "q" }).
    //     addAccidental(1, new Vex.Flow.Accidental("b")).
    //     addAccidental(2, new Vex.Flow.Accidental("#"))
];

function addNote(data) {
    if (data.length == 0)
        return;

    var note     = data[0][0][0];
    var octave   = data[0][0][1];
    var duration = data[0][2];
    
    var newNote = new Vex.Flow.StaveNote({ keys: [note + "/" + octave], duration: "" + duration });
    if (note.length > 1)
        newNote.addAccidental(0, new Vex.Flow.Accidental(note.substring(1)));
    notes.push(newNote);
    draw();
}
function draw() {
    // Helper function to justify and draw a 4/4 voice
    canvas.width = canvas.width;
    stave.draw();
    Vex.Flow.Formatter.FormatAndDraw(ctx, stave, notes);
    //voice.draw(ctx, stave);
}
draw();
