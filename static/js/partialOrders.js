let EVENT_WIDTH = 125
let textWidthMap = new Map()
axios.get('/partial-order/po-groups')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data['metadata']['colors']))

            let longestActivityWidth = getLongestActivityWidth(response.data['metadata']['longestActivityName'], '#partial-order-0')
            if (longestActivityWidth > EVENT_WIDTH) {
                EVENT_WIDTH = longestActivityWidth
            }

            let partialOrderGroups = response.data['groups']
            let groupKeys = Object.keys(partialOrderGroups)
            for (let i = 0; i < groupKeys.length; i++) {
                drawPartialOrders(i, partialOrderGroups[groupKeys[i]][EVENTS_KEY], colorMap)
            }
        }
    );

function drawPartialOrders(groupNumber, events, colorMap) {
    let partialOrders = []
    let maxParallelEvents = 1
    for (let i = 0; i < events.length;) {
        let parallelEvents = [events[i]]
        let j = 1
        for (; i + j < events.length; j++) {
            if (events[i][TIMESTAMP_KEY] === events[i + j][TIMESTAMP_KEY]) {
                parallelEvents.push(events[i + j])
            } else {
                break
            }
        }
        if (parallelEvents.length > maxParallelEvents) {
            maxParallelEvents = parallelEvents.length
        }
        partialOrders.push(parallelEvents)
        i = i + j
    }

    let height = maxParallelEvents * EVENT_HEIGHT + (maxParallelEvents - 1) * GAP

    let svg = d3.selectAll(`#partial-order-${groupNumber}`).append("svg").attr("height", height)
    $(`#partial-order-${groupNumber}`).click(function () {
        redirectPost("/partial-order/combinations", {
            "partialOrder": JSON.stringify(events)
        })
    })
    drawPartialOrder(svg, partialOrders, maxParallelEvents, colorMap)
}

function drawPartialOrder(svg, eventList, maxParallelEvents, colorMap) {
    let baseY
    if (maxParallelEvents % 2 === 0) {
        baseY = (maxParallelEvents / 2 - 0.5) * (EVENT_HEIGHT + GAP)
    } else {
        baseY = Math.floor(maxParallelEvents / 2) * (EVENT_HEIGHT + GAP)
    }

    let xOffset = 0
    let i = 0
    for (i; i < eventList.length; i++) {
        if ((i !== 0 && eventList[i].length % 2 === 0 && (eventList[i - 1].length % 2 !== 0)) ||
            (i !== 0 && eventList[i].length % 2 !== 0 && (eventList[i - 1].length % 2 === 0))
        ) {
            xOffset = xOffset + GAP * 3
        }
        for (let j = 0; j < eventList[i].length; j++) {
            let activityName = eventList[i][j][ACTIVITY_KEY];
            let yOffset
            if (eventList[i].length % 2 === 0) {
                yOffset = (eventList[i].length / 2 - 0.5) - j
            } else {
                yOffset = Math.floor(eventList[i].length / 2) - j
            }

            let polygon
            if (i === 0) {
                // starting events do not have a corner on the left
                polygon = `${xOffset + i * (EVENT_WIDTH + GAP)},${baseY - (yOffset * (EVENT_HEIGHT + GAP))} ${(xOffset + EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},${baseY - (yOffset * (EVENT_HEIGHT + GAP))} ${xOffset + EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT / 2} ${xOffset + EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT} ${xOffset + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT}`
            } else {
                // standard event, not starting and finishing
                polygon = `${xOffset + i * (EVENT_WIDTH + GAP)},${baseY - (yOffset * (EVENT_HEIGHT + GAP))} ${(xOffset + EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},${baseY - (yOffset * (EVENT_HEIGHT + GAP))} ${xOffset + EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT / 2} ${xOffset + EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT} ${xOffset + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT} ${xOffset + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT / 2}`
            }

            svg.append('polygon')
                .attr('points', polygon)
                .attr('class', 'event')
                .attr('fill', colorMap.get(activityName))

            if (!textWidthMap.has(activityName)) {
                let text = svg.append('text')
                    .text(activityName)

                textWidthMap.set(activityName, text.node().getComputedTextLength())
                text.remove()
            }

            if (i === 0) {
                svg.append('text')
                    .attr('x', xOffset + i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH) / 2) - textWidthMap.get(activityName) / 2)
                    .attr('y', baseY - (yOffset * (EVENT_HEIGHT + GAP)) + 31)
                    .text(activityName)
            } else {
                svg.append('text')
                    .attr('x', xOffset + i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH + EVENT_DIAMETER) / 2) - textWidthMap.get(activityName) / 2)
                    .attr('y', baseY - (yOffset * (EVENT_HEIGHT + GAP)) + 31)
                    .text(activityName)
            }
        }
    }
    let width = xOffset + i * (EVENT_WIDTH + GAP) + EVENT_DIAMETER - GAP + STROKE_SPACE
    svg.attr("width", width)
}