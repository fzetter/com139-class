// Config
// ******

const datap = pie_json
const widthp = $("#pie-chart").width() / 2 - 10
const heightp = $("#pie-chart").height() / 2
const radiusp = Math.min(widthp, heightp)
const gp = d3.select("#pie-chart").append("g")
.attr("transform", "translate(" + (widthp / 2 + margin.left + 10) + "," + (heightp / 2 + margin.bottom + 30) + ")")

// Scale, Arc Generator & Pie Layout
const color = d3.scaleOrdinal().domain(Object.keys(datap)).range(d3.schemePaired.splice(0,12))
const arc = d3.arc().outerRadius(radiusp).innerRadius(0)
const pie = d3.pie().value(d => d.value).sort(null)

// Pie
gp
  .selectAll('chart')
  .data(pie(d3.entries(datap)))
  .enter()
  .append('path')
  .attr('d', arc)
  .attr('fill', d => color(d.data.key))
  .attr("stroke", "black")
  .style("stroke-width", "1px")
  .style("opacity", 0.7)

/* Legend
const rectSize = 20, spacing = 10
const legendp = gp.selectAll('.legend').data(color.domain())

legendp.exit().remove()

legendp.enter()
  .append('g')
  .merge(legendp)
  .attr('class', 'legend')
  .attr('transform', function(d, i) {
    const height = rectSize + spacing
    const offset =  height * color.domain().length / 2
    const horz = width / 2
    const vert = i * height - offset
    return 'translate(' + (i-20) + ',' + (i*height-100) + ')'
  })
  .append('rect')
    .attr('width', rectSize)
    .attr('height', rectSize)
    .style('fill', color)
    .style('stroke', color)

  gp.selectAll('.legend').append('text')
    .merge(legendp)
    .attr('x', spacing + 20)
    .attr('y', rectSize - spacing)
    .attr("font-size", "10px")
    .style('fill', "#000")
    .text(d => d)
*/
