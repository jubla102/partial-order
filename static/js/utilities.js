const EVENT_HEIGHT = 50
const GAP = 4
const EVENT_DIAMETER = 10
const EVENTS_KEY = 'events'
const ACTIVITY_KEY = 'concept:name'
const TIMESTAMP_KEY = 'time:timestamp'
const STROKE_SPACE = 4

function getTextWidth(text) {
    let svg = d3.select('#text-width-calculation').append("svg")
    let textObj = svg.append('text')
        .attr('opacity', 0)
        .text(text)
    let textWidth = textObj.node().getComputedTextLength()
    textObj.remove()

    // +4 is added to compensate for the deviation of getComputedTextLength()
    return textWidth + 4;
}