document.addEventListener('DOMContentLoaded', function() {
  const data = [10, 20, 30, 40, 50]; // Sample data
  const svgWidth = 400, svgHeight = 400;
  const radius = Math.min(svgWidth, svgHeight) / 2;

  const svg = d3.select('body').append('svg')
      .attr('width', svgWidth)
      .attr('height', svgHeight);

  // Create group element to hold pie chart
  const g = svg.append('g')
      .attr('transform', `translate(${svgWidth / 2}, ${svgHeight / 2})`);

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const pie = d3.pie();

  const arc = d3.arc()
      .innerRadius(0)
      .outerRadius(radius);

  const arcs = g.selectAll('arc')
      .data(pie(data))
      .enter()
      .append('g')
      .attr('class', 'arc');

  arcs.append('path')
      .attr('fill', (d, i) => color(i))
      .attr('d', arc);
});
