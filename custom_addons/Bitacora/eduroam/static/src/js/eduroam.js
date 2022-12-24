$(".copy").on("click", function (ev) {
    let parent = $(ev.currentTarget).parent()
    let data = parent.find('div')
    CopyToClipboard(data[0])

    $(ev.currentTarget).html("Copiado!")
    setTimeout(() => {
        $(ev.currentTarget).html("Copiar")
    },1200)


})

function CopyToClipboard(obj) {
    var r = document.createRange();
    r.selectNode(obj);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(r);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
}