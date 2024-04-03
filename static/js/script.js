document.addEventListener("DOMContentLoaded", function () {
    window.addEventListener('scroll', reveal);
    reveal();
});

function reveal() {
    var reveals = document.querySelectorAll('.animated-section');
    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var revealTop = reveals[i].getBoundingClientRect().top;
        var revealPoint = 50;

        if (revealTop < windowHeight - revealPoint) {
            reveals[i].classList.add('animate');
        } else {
            reveals[i].classList.remove('animate');
        }
    }
}
