// create svg element:
// todo: the width must be some multiple of the longest trace
var svg = d3.selectAll(".rect").append("svg").attr("width", 8000).attr("height", 200)

hospitalData = [
    {
        name: 'Registration',
        color: '#69b3a2'
    },
    {
        name: 'Leucocytes',
        color: '#bc5090'
    },
    {
        name: 'CRP',
        color: '#ff6361'
    },
    {
        name: 'IV Liquid',
        color: '#ffa600'
    },
    {
        name: 'LacticAcid',
        color: '#69a3b2'
    },
    {
        name: 'Birth',
        color: '#69a3b2'
    },
    {
        name: 'Death',
        color: '#69a3b2'
    },
    {
        name: 'Julian',
        color: '#69a3b2'
    },
    {
        name: 'A',
        color: '#69a3b2'
    },
    {
        name: 'B',
        color: '#69a3b2'
    },
    {
        name: 'C',
        color: '#69a3b2'
    },
    {
        name: 'D',
        color: '#69a3b2'
    },
    {
        name: 'E',
        color: '#69a3b2'
    }

]

var tooltip = d3.select("body")
    .append("div")
    .attr('class', 'tooltipdiv')
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .text("a simple tooltip");

// first chevron activity
svg.append('polygon')
    .attr('points', "50,50 150,50 175,75 150,100 50,100")
    .attr('fill', '#69b3a2')

svg.append('text')
    .attr('x', 70)
    .attr('y', 80)
    .attr('stroke', 'black')
    .text("ER Sepsis")


//Following activities
for (let i = 1; i < hospitalData.length; i++) {
    svg.append('polygon')
        .attr('points', `${50 + i * 110},50 ${150 + i * 110},50 ${175 + i * 110},75 ${150 + i * 110},100 ${50 + i * 110},100 ${75 + i * 110},75`)
        .attr('fill', hospitalData[i].color)

    /*todo: mouseover is working but is very annoying: remove alert, think of pop-up like this(http://jsfiddle.net/thatOneGuy/7NReF/36/)
    .on("mouseover", function (d, i) {
        alert("The details are:\n" + "Name:" +
            hospitalData[i].name + "\n" + "Color:" + hospitalData[i].color);
    })*/

    svg.append('text')
        .attr('x', 80 + i * 110)
        .attr('y', 80)
        .attr('stroke', 'black')
        .text(hospitalData[i].name)


}

