let startingIndexOfLeftRight = 0;
let isTutorial = true;
//var data = [["Yeşil", "Tatlı", "Karpuz"],['Yeşil', "Ekşi", 'Elma'], ['Kırmızı', "Tatlı", 'Elma'], ['Sarı', "Ekşi", 'Limon']]

const data = [
              ["Trion Lannister", "Hayır", "Yok", "İstemiyor", "Sarı", "Lannister"],
              ["Daenerys Targaryen", "Evet", "Var", "İstiyor", "Beyaz", "Targaryen"],
              ["John Snow", "Hayır", "Yok", "İstemiyor", "Siyah", "Stark"],
              ["Cercei Lannister", "Evet", "Yok", "İstiyor", "Sarı", "Lannister"],
              ["Night King", "Hayır", "Var", "İstemiyor", "Beyaz", "White Walker"],
              ["Jamie Lannister", "Evet", "Yok", "İstemiyor",  "Sarı", "Lannister"],
              ["Arya Stark", "Hayır", "Yok", "İstemiyor", "Siyah", "Stark"],
              ["Tywin Lannister", "Evet", "Yok", "İstiyor",  "Sarı", "Lannister"],
              ["Sansa Stark", "Hayır", "Yok", "İstemiyor", "Kızıl", "Stark"],
              ["Lieutenant White Walkers", "Hayır", "Var", "İstemiyor", "Beyaz", "White Walker"],
              ["Viserys Targaryen", "Hayır", "Yok",  "İstiyor", "Beyaz", "Targaryen"],
              ["Wights", "Hayır", "Yok", "İstemiyor", "Beyaz", "White Walker"],
              ["Eddard Stark", "Hayır", "Yok", "İstemiyor", "Siyah", "Stark"],
            ];
const reducedData = [
              ["Daenerys Targaryen", "Evet", "Var", "İstiyor", "Beyaz", "Targaryen"],
              ["John Snow", "Hayır", "Yok", "İstemiyor", "Siyah", "Stark"],
              ["Cercei Lannister", "Evet", "Yok", "İstiyor", "Sarı", "Lannister"],
              ["Night King", "Hayır", "Var", "İstemiyor", "Beyaz", "White Walker"],
              ["Jamie Lannister", "Evet", "Yok", "İstemiyor",  "Sarı", "Lannister"],
              ["Arya Stark", "Hayır", "Yok", "İstemiyor", "Siyah", "Stark"],
              ["Lieutenant White Walkers", "Hayır", "Var", "İstemiyor", "Beyaz", "White Walker"],
              ["Eddard Stark", "Hayır", "Yok", "İstemiyor", "Siyah", "Stark"],
            ];
const colorMap = {"Lannister": "#7C6248", "Targaryen": "#EAFAFD", "Stark": "#8C94A1", "White Walker": "#3A81ED"};

const dict = {};
const questions = {"Zengin mi?": {attribute: "Evet", type: 1},
      "Beyaz saçlı mı?": {attribute: "Beyaz", type: 4},
      "Ejderhası var mı?": {attribute: "Var", type: 2}};
const labelToImage = {"Stark" : "stark.png", "Targaryen" : "targaryen.png", "Lannister": "lannister.png"};
const whiteWalkerImage = {"Night King" : "night_king.jpg", "Wights": "wights.jpg", "Lieutenant White Walkers": "lieutenant.jpg"};
const descriptions = ["Game of Thrones dizisinin karakterleri, onların özellikleri ve üyesi oldukları haneyi görüyorsunuz   ",
                  "Belirtilen kısımdaki sorulara tıklayarak verilerinizi ikiye ayırabilirsiniz",
                  "Veriler sorduğunuz soruya göre ikiye ayrıldı",
                  "Bu karmaşıklık değeri 'Evet' kısmındaki verilerin karmaşıklığını ifade eder",
                  "Bu karmaşıklık değeri ise 'Hayır' kısmındaki verilerin karmaşıklığını ifade eder",
                  "Verilerinizdeki tamamındaki karmaşıklık oranı burada gösterilmektedir",
                  "Bu soruyu sormakla elde edeceğiniz karmaşıklığı azalma miktarı 'sorunun skoru' olarak belirtilmektedir",
                  "Farklı özellikleri deneyerek en iyisi skoru veren soruyu bulun. Karakterleri 'Evet' veya 'Hayır' alanlarına sürükleyerek işe başlayabilirsiniz",
                  "Verilerinizi bu şekilde yukarıda eleman kalmayana kadar bölün ve en son sorunun skorunu hesaplamak için Hesapla butonuna tıklayınız. Resetle butonu ile verileri geri yukarı taşıyabilirsiniz"];
function calculateEntropy(data){
  const totalNumber = data.length;
  const labelDict = {};
  for (let i in data){
    //get the last column which is the label
    const entry = data[i];
    const decision = entry[entry.length - 1];
    if( decision in labelDict){
        labelDict[decision]++;
    } else {
        labelDict[decision] = 1.0
    }
  }
  let entropy = 0.0;
  for(let key in labelDict){
      let prob = labelDict[key] / totalNumber;
      entropy -= prob * Math.log2(prob);
  }
  return entropy
}

//Fill in the main_list
function loadDataIntoMainList(data){
    data.forEach((entry, i) => {
        let obje = { attributeValues : entry};
        let text = "";
        const $tr = $("<tr>");
        $tr.addClass("text-center");
        for(let attribute in entry) {
            text += entry[attribute] + "  ";
            $tr.append("<td>" + entry[attribute] + "   </td>");
        }
        let label = entry[entry.length - 1];
        $tr.css("background-color", colorMap[label]);

        if(label !== "White Walker") {
            $tr.append("<img src = '../icons/" + labelToImage[label] + "' width = '50'>")
        } else {
            $tr.append("<img src = '../icons/" + whiteWalkerImage[entry[0]] + "' width = '50'>")
        }

        const $newNode = $tr.attr("id", "entry_" + i);
        dict[$newNode.attr("id")] = obje;
        $("#main_list > tbody").append($newNode);
    });
}
//General calculateEntropyById, excludes first item haaaaaaaaaaaaaa
function calculateEntropyById(id){
    let leftData = [];
    let leftItems = $(id);
    for(let i = startingIndexOfLeftRight; i < leftItems.length; i++){
        const $item = $(leftItems[i]);
        const tokens = dict[$item.attr("id")]["attributeValues"];
        leftData.push(tokens)
    }
    return calculateEntropy(leftData)
}
//Send left and right back toto main_list
function resetLeftRight(){
    const leftItems = $("#left tbody tr");
    for(let i = startingIndexOfLeftRight; i < leftItems.length; i++){
       const $item = $(leftItems[i]);
       $("#main_list tbody").append($("#" + $item.attr("id")))
    }
    let rightItems = $("#right tbody tr");
    for(let i = startingIndexOfLeftRight; i < rightItems.length; i++){
       const $item = $(rightItems[i]);
       $("#main_list tbody").append($("#" + $item.attr("id")))
    }
}
//Reset left and right but send new list to main_list
function resetLeftRightAddNewList(){
    $("#left tbody").html("");
    $("#right tbody").html("");
    $("#main_list tbody").html("");
    loadDataIntoMainList(reducedData)
}
function resetEntropyValues(){
    $("#leftEntropy, #rightEntropy").html("Karmaşıklık: -");
    $("#averageEntropy").html("Ortalama Karmaşıklık: -");
    $("#totalGain").html("Bu sorunun skoru: -");
}
//recalculates entropy of the left and right divs
function recalculateLeftRight(){
    //left
    let leftEntropy = calculateEntropyById("#left tbody tr");
    //right
    let rightEntropy = calculateEntropyById("#right tbody tr");
    $("#leftEntropy").html("Karmaşıklık: " + leftEntropy.toFixed(2));
    $("#rightEntropy").html("Karmaşıklık: " + rightEntropy.toFixed(2));
    console.log("Left: ", leftEntropy, "Right: ", rightEntropy);
}
//This function is called when the Document is loaded
$( function() {
    const $overlay_button = $("#overlay_button");
    const $overlay_text = $("#overlay_text");
    const $error = $("#error");
    loadDataIntoMainList(data);
    //tutorial section
    let descIndex = 0;
    $(".a0 .a1").css("z-index", 999);
    $overlay_text.html(descriptions[descIndex]);
    descIndex++;
    $overlay_button.click(()=>{
        $overlay_text.html(descriptions[descIndex]);
        if(descIndex === 1){
            $(".a0 .a1").css("z-index", 0);
            $(".a0 .a2").css("z-index", 999);
            $overlay_button.css("display", "none");
            document.getElementById("question_list").scrollIntoView()
        } else if(descIndex === 3) { // == 2 is handled by question buttons
            $(".c0 .c1").css("z-index", 0);
            $(".d0 .d1").css("z-index", 999);
            document.getElementById("leftEntropy").scrollIntoView()
        } else if(descIndex === 4){
            $(".d0 .d1").css("z-index", 0);
            $(".d0 .d2").css("z-index", 999)
        } else if (descIndex === 5){
            $(".d0 .d2").css("z-index", 0);
            $(".f0").css("z-index", 999)
        } else if (descIndex === 6){
            $(".f0").css("z-index", 0);
            $(".g0 .g1").css("z-index", 999)
        } else if(descIndex === 7){
            $(".g0 .g1").css("z-index", 0);
            $overlay_text.css("top", "50%");
            $overlay_text.css("left", "77%");
            $overlay_button.css("top", "80%");
            $overlay_button.css("right", "30%");
            $(".overlay").css("display", "none");
            isTutorial = false;
        } else if(descIndex === descriptions.length - 1){
            $(".b0 .b1").css("z-index", 0);
            $(".overlay").css("display", "none");
            isTutorial = false;
        }
        descIndex++;
    });
    //tutorial section ended

    //questions are layed out
    for (let question in questions){
        const button = document.createElement("button");
        const $button = $(button);
        $button.css("margin-top", "10px").css("width", "200px").addClass("btn").addClass("btn-primary").addClass("btn-lg").html(question).appendTo("#question_list");
        $button.click((function(question) {return function() {
            resetLeftRight();
            resetEntropyValues();
            const mainItems = $("#main_list tbody tr");
            for(let i = 0; i < mainItems.length; i++){
                const $item = $(mainItems[i]);
                const conditionAttribute = dict[$item.attr("id")]["attributeValues"][question["type"]];
                if(conditionAttribute === question["attribute"]){
                    $("#left").append($("#" + $item.attr("id")));
                }else{
                    $("#right").append($("#" + $item.attr("id")));
                }
            }
            const totalNumber = mainData.length;//left
            const leftEntropy = calculateEntropyById("#left tbody tr");
            const leftSize = $("#left tbody tr").length - 1;
            //right
            const rightEntropy = calculateEntropyById("#right tbody tr");
            const rightSize = $("#right tbody tr").length - 1;
            const averageEntropy = (leftSize / totalNumber) * leftEntropy + (rightSize / totalNumber) * rightEntropy;
            $("#averageEntropy").html("Ortalama Entropi: " + averageEntropy.toFixed(2));
            const gain = mainEntropy - averageEntropy;
            $("#totalGain").html("Bu sorunun skoru: " + gain.toFixed(2));
            recalculateLeftRight();
            if(isTutorial){
                $(".a0 .a2").css("z-index", 0);
                $(".c0 .c1").css("z-index", 999);
                $overlay_text.css("right", "5%");
                $overlay_text.css("top", "80%");
                $overlay_button.css("top", "90%");
                $overlay_text.html(descriptions[descIndex]);
                $overlay_button.css("display", "block");
                descIndex++;
            }
        };})(questions[question]));
    }

    //Calculate main entropy
    let mainData = [];
    const mainItems = $("#main_list tbody tr");
    for(let i = 0; i < mainItems.length; i++){
        const $item = $(mainItems[i]);
        const tokens = dict[$item.attr("id")]["attributeValues"];
        mainData.push(tokens)
    }
    const mainEntropy = calculateEntropy(mainData);
    $("#mainEntropy").html("Sistemin Karmaşıklığı: " + mainEntropy.toFixed(2));


    //Define method when drag&drop completed
    function onStopSorting(){
        if(isTutorial){
            $overlay_text.html(descriptions[descIndex]);
            $(".a0 .a1").css("z-index", 0);
            $(".c0 .c1").css("z-index", 0);
            $(".b0 .b1").css("z-index", 999);
            $overlay_button.css("display", "block");
        }

        resetEntropyValues();
        let $main_list = $("#main_list tbody");
        if($main_list[0].childElementCount === 0){
            recalculateLeftRight()
        }
    }
    $("#calculate").click(()=>{
        //It is important that all elements in main_list is moved partially to left and right
        if ($("#main_list tbody")[0].childElementCount === 0) {
            let leftList = $("#left tbody tr");
            let featuresMatrix = [];
            for(let i = 0; i < leftList.length; i++){
                const $item = $(leftList[i]);
                let attributeArr = dict[$item.attr("id")]["attributeValues"];
                featuresMatrix.push([]);
                for(let j = 0; j < attributeArr.length; j++){
                    featuresMatrix[i].push(attributeArr[j])
                }
            }

            let validSplit = false;
            let col;
            //col started from 1 so that name is not taken into account
            for(col = 1; featuresMatrix.length !== 0 && col < featuresMatrix[0].length - 1 && !validSplit; col++){
                let previous = featuresMatrix[0][col];// first element is previous
                let differentFound = false;
                for(let row = 1; !differentFound && row < featuresMatrix.length; row++){
                    if(featuresMatrix[row][col] !== previous){
                        differentFound = true;
                    }
                }
                if(!differentFound){
                    //Let's check if the same column is valid in the right list
                    let rightItems = $("#right tbody tr");
                    if(rightItems.length > 0) {
                        let sameFound = false;
                        for (let i = 0; i < rightItems.length; i++) {
                            const $rightItem = $(rightItems[i]);
                            const current = dict[$rightItem.attr("id")]['attributeValues'][col];
                            if(current === previous){
                                sameFound = true;
                            }
                        }
                        validSplit = !sameFound
                    } else {
                        validSplit = true
                    }
                }
            }
            if(validSplit) {
                let totalNumber = mainData.length;
                const leftEntropy = calculateEntropyById("#left tbody tr");
                const leftSize = $("#left tbody tr").length - 1;
                //right
                const rightEntropy = calculateEntropyById("#right tbody tr");
                const rightSize = $("#right tbody tr").length - 1;
                let averageEntropy = (leftSize / totalNumber) * leftEntropy + (rightSize / totalNumber) * rightEntropy;
                $("#averageEntropy").html("Ortalama Entropi: " + averageEntropy.toFixed(2));
                let gain = mainEntropy - averageEntropy;
                $("#totalGain").html("Bu sorunun skoru: " + gain.toFixed(2))
            }  else {
                $error.html("Verilerinizi herhangi bir soruya veya ortak özelliğe göre bölmediniz bu yüzden skor hesaplanamadı.");
                $error.slideDown().delay(5000).slideUp();
            }
        } else {
            $error.html("Bütün elemanlar paylaştırılmadan sorunun skoru hesaplanamaz");
            $error.slideDown().delay(5000).slideUp();
        }
    });
    $("#reset").click(()=>{
        resetLeftRight();
        resetEntropyValues();
    });
    $("#proceed").click(()=>{
        resetEntropyValues();
        resetLeftRightAddNewList();
        startingIndexOfLeftRight = 0;
        $("#proceed").css("display", "none");
        $("#question_list").css("display", "none");
        $("#reset").css("display", "inline-block");
        $("#calculate").css("display", "inline-block");
        //$("#left li:first-child, #right li:first-child").css("background-color", "orange")
        $('#right tbody tr, #left tbody tr, #main_list tbody tr').draggable({
            connectToSortable: ".sortable",
            revert: 'invalid',
            drag: function( event, ui ) {
                $(ui.helper).css("position", "absolute")
            },
            stop: function( event, ui ) {
                $(ui.helper).css("position", "")
            }
        });
        $('#left, #right').sortable({
            stop: onStopSorting,
            items: "#left tbody tr, #right tbody tr"
        });
        $("#main_list, #left, #rigth").disableSelection();
        //Tutorial part
        $(".overlay").css("display", "block");
        $(".a0 .a1").css("z-index", 999);
        $(".c0 .c1").css("z-index", 999);
        $overlay_button.css("display", "none");
        isTutorial = true
    })
});