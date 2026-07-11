class WebPage {
    constructor(title, headline, id, body) {
        this.title = title;
        this.headline = headline;
        this.id = id;
        this.body = body;
    }
}

const pageList = [new WebPage(
    title = 'About',
    headline = 'About',
    id = 'aboutLink',
    body = 'Uplink devices extract the data you need to make the best decisions possible\
    <iframe style="padding-top: 40px;" src="https://app.vectary.com/p/5CCeIGgL57lEG4hEoP7akD" frameborder="0" width="100%" height="240"></iframe>\
    <iframe width="560" height="315" src="https://www.youtube.com/embed/k2vQDvNeh2s?si=qCTEF3pleOAV_2h5&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
), new WebPage(
    title = 'Contact',
    headline = 'Contact',
    id = 'contactLink',
    body = "Reach out to <a href='mailto:nick@advin.io'>Nick</a> with your questions"
)];

function changePage(document, newPage) {
    const headline = document.getElementById('headline');

    // Make sure not on page already
    if (headline === null || newPage.headline === headline.textContent) {
        return;
    }

    const body = document.getElementById('body');
    if (body === null) {
        return;
    }

    // First phase = fade out and shrink
    headline.classList.add('fade-out-and-shrink');
    body.classList.add('fade-out-and-shrink');

    // Wait for the fade-out animation to complete
    setTimeout(() => {
        // Update the text after the first text has faded out
        headline.textContent = newPage.headline;
        body.innerHTML = newPage.body;

        // Remove the fade-out class
        headline.classList.remove('fade-out-and-shrink');
        body.classList.remove('fade-out-and-shrink');

        // Trigger reflow to restart the animation
        void headline.offsetWidth;
        void body.offsetWidth;

        // Second phase = fade in and grow
        headline.classList.add('fade-in-and-grow');
        body.classList.add('fade-in-and-grow');

        // Wait for the fade-in animation to complete
        setTimeout(() => {
            headline.classList.remove('fade-in-and-grow');
            body.classList.remove('fade-in-and-grow');
        }, 1000); // This duration should match the fade-in-and-grow animation duration
    }, 1000); // This duration should match the fade-out-and-shrink animation duration
}

document.addEventListener('DOMContentLoaded', () => {
    for (let i = 0; i < pageList.length; i++) {
        if (pageList[i].id === null) {
            console.log(`Page ${i} has no id`);
        }
        document.getElementById(pageList[i].id).addEventListener('click', () => changePage(document, pageList[i]));
    }
});
