const EVENT_HEIGHT = 50
const GAP = 4
const EVENT_DIAMETER = 10
const EVENTS_KEY = 'events'
const ACTIVITY_KEY = 'concept:name'
const TIMESTAMP_KEY = 'time:timestamp'
const STROKE_SPACE = 4

function redirectPost(url, data) {
    let form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = url;
    for (let name in data) {
        let input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = data[name];
        form.appendChild(input);
    }
    form.submit();
}

function getTextWidth(text) {
    let svg = d3.select('#text-width-calculation').append("svg")
    let textObj = svg.append('text')
        .attr('opacity', 0)
        .text(text)
    let textWidth = textObj.node().getComputedTextLength()
    textObj.remove()

    return textWidth;
}