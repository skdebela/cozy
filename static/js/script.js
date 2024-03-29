// script for the destination details

document.getElementById('show-more').addEventListener('click', function (event) {
    event.preventDefault();
    document.getElementById('more-plot').style.display = 'block';
    this.style.display = 'none';
    document.getElementById('show-less').style.display = 'inline';
});

document.getElementById('show-less').addEventListener('click', function (event) {
    event.preventDefault();
    document.getElementById('more-plot').style.display = 'none';
    document.getElementById('show-more').style.display = 'inline'
    this.style.display = 'none';button
});

