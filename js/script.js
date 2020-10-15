$(document).ready(function() {
    $("form").on('keyup keypress', function(event) {
        if (event.keyCode === 13) {
            document.getElementById("btn").classList.toggle("clicked");
            $("#btn").click();
            return false;
        }
    });

    $("#btn").click(function() {
        name = document.getElementById("nome").value;
        nameToDisplay = name.toUpperCase();
        name = name.toLowerCase();

        for (let tuple in name_meaningJSON.meaning_pearson) {
            var lenght = tuple
        }

        for (var i = 0; i < lenght + 1; i++) {
            try {
                nome = name_meaningJSON.meaning_pearson[i].nome;

                if (name == nome) {
                    var meaning = name_meaningJSON.meaning_pearson[i].meaning;
                }
            } catch {
                continue;
            }

        }

        if (meaning === undefined) {
            meaning = 'Ainda não sei o significado do nome "' + name + '" mas estou sempre aprendendo...'
        }

        divP = document.getElementById("result-p");
        divP.style.display = "block";
        document.getElementById("meaning-p").innerHTML = "<strong>" + nameToDisplay + ": </strong>" + meaning;
    });
});