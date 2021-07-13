// Config
const margin = {top: 10, right: 10, bottom: 100, left: 100}
const width = 550, height = 500, radius = Math.min(width, height) / 2

const g = d3.select("#chart-area")
	.append("svg")
		.attr("width", width + margin.right + margin.left)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

// Scale, Arc Generator & Pie Layout
const color = d3.scaleOrdinal().range(d3.schemeDark2)
const arc = d3.arc().outerRadius(radius - 20).innerRadius(radius - 100)
const pie = d3.pie().value(d =>  d.count).sort(null)

// Parse Data
data.forEach(d => d.count = +d.count)
console.log(data)

const regionsByFruit = d3.nest().key(d => d.fruit).entries(data).reverse()
const label = d3.select("form").selectAll("label").data(regionsByFruit).enter().append("label")

// Radio Buttons
label.append("input")
        .attr("type", "radio")
        .attr("name", "fruit")
        .attr("value", d => d.key)
        .on("change", update)
    .filter((d, i) => !i)
        .each(update)
        .property("checked", true)

label.append("span").attr("fill", "red").text(d => d.key)

// Update Chart
function update(region) {
    let path = g.selectAll("path")
    let data0 = path.data()
    let data1 = pie(region.values)
    let t = 750

    // JOIN elements with new data.
    path = path.data(data1, key)

    // EXIT old elements from the screen.
    path.exit()
        .datum((d, i) => findNeighborArc(i, data1, data0, key) || d)
        .transition()
        .duration(t)
        .attrTween("d", arcTween)
        .remove()

    // UPDATE elements still on the screen.
    path.transition()
        .duration(t)
        .attrTween("d", arcTween)

    // ENTER new elements in the array.
    path.enter()
        .append("path")
        .each((d, i) => {
        	this._current = findNeighborArc(i, data0, data1, key) || d
        })
        .attr("fill", d => color(d.data.region))
        .transition()
        .duration(t)
        .attrTween("d", arcTween)
}

function key(d) { return d.data.region }

function findNeighborArc(i, data0, data1, key) {
    let d
    return (d = findPreceding(i, data0, data1, key)) ? {startAngle: d.endAngle, endAngle: d.endAngle}
        : (d = findFollowing(i, data0, data1, key)) ? {startAngle: d.startAngle, endAngle: d.startAngle}
        : null
}

// Find the element in data0 that joins the highest preceding element in data1.
function findPreceding(i, data0, data1, key) {
    let m = data0.length
    while (--i >= 0) {
        let k = key(data1[i])
        for (let j = 0; j < m; ++j) {
            if (key(data0[j]) === k) return data0[j]
        }
    }
}

// Find the element in data0 that joins the lowest following element in data1.
function findFollowing(i, data0, data1, key) {
    let n = data1.length, m = data0.length
    while (++i < n) {
        let k = key(data1[i])
        for (let j = 0; j < m; ++j) {
            if (key(data0[j]) === k) return data0[j]
        }
    }
}

function arcTween(d) {
    let i = d3.interpolate(this._current, d)
    this._current = i(1)
    return t => arc(i(t))
}
