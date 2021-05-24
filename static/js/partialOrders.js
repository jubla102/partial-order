// create svg element:
var svg = d3.selectAll(".rect").append("svg").attr("width", 800).attr("height", 200)

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
        name: 'Avinash',
        color: '#69a3b2'
    }
]

svg.append('polygon')
    .attr('points', "50,50 150,50 175,75 150,100 50,100")
    .attr('fill', '#69b3a2')

svg.append('text')
    .attr('x', 70)
    .attr('y', 80)
    .attr('stroke', 'black')
    .text("ER Sepsis")

for (let i = 1; i < hospitalData.length; i++) {
    svg.append('polygon')
        .attr('points', `${50 + i * 110},50 ${150 + i * 110},50 ${175 + i * 110},75 ${150 + i * 110},100 ${50 + i * 110},100 ${75 + i * 110},75`)
        .attr('fill', hospitalData[i].color)

    svg.append('text')
        .attr('x', 80 + i * 110)
        .attr('y', 80)
        .attr('stroke', 'black')
        .text(hospitalData[i].name)
}

