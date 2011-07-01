function getRandomInt(min, max)
{
return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getNiceResult(){
    var r = getRandomInt(0, 10);
    if(r>=0 && r<2){
        return 0;
    }
    if(r>=2 && r<=4){
        return 1;
    }
    if(r>=5 && r<=7){
        return 2;
    }
    if(r>=8 && r<=9){
        return 3;
    }
    if(r==10){
        return 4;
    }
}

function assignRandom(input){
    input.val(getNiceResult()+"");
}

function assignRandomFirstRound(){
    var goals_field = $(".goals-field");
    goals_field.each(function(){
        $(this).val(getNiceResult()+"");
    });   
}

function assignRandomFinalRound(){
    var goals_field = $(".goals-field");
    for(var i=0; i< goals_field.length; i+=2){
        var res1= getNiceResult();
        var res2= getNiceResult();
        if(res1==res2){
            res1+=1;
        }
        $(goals_field[i]).val(res1);
        $(goals_field[i+1]).val(res2);
    }
}