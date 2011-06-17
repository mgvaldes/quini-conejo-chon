team_acronym ={
    'Argentina':'Arg',
    'Colombia':'Col',
    'Costa Rica':'Cos',
    'Bolivia':'Bol',
    'Brasil':'Bra',
    'Venezuela':'Ven',
    'Ecuador':'Ecu',
    'Paraguay':'Par',
    'Uruguay':'Uru',
    'Peru':'Per',
    'Mexico':'Mex',
    'Chile':'Chi'
};
    
team_long={
    "Arg":"Argentina",
    "Col":"Colombia",
    "Cos":"Costa Rica",
    "Bol":"Bolivia",
    "Bra":"Brasil",
    "Ven":"Venezuela",
    "Ecu":"Ecuador",
    "Par":"Paraguay",
    "Uru":"Uruguay",
    "Per":"Peru",
    "Mex":"Mexico",
    "Chi":"Chile"
    }
    
// group matches hash
matches_hash = {
    'A': {
        'Arg': ['Arg-Bol', 'Arg-Cos', 'Arg-Col'],
        'Col': ['Col-Cos', 'Arg-Col', 'Col-Bol'],
        'Bol': ['Arg-Bol', 'Bol-Cos', 'Col-Bol'],
        'Cos': ['Col-Cos', 'Bol-Cos', 'Arg-Cos']
    },
    'B': {
        'Bra': ['Bra-Ven', 'Bra-Par', 'Bra-Ecu'],
        'Par': ['Par-Ecu', 'Bra-Par', 'Par-Ven'],
        'Ecu': ['Par-Ecu', 'Ven-Ecu', 'Bra-Ecu'],
        'Ven': ['Bra-Ven', 'Ven-Ecu', 'Par-Ven']
    },
    'C': {
        'Chi': ['Chi-Mex', 'Uru-Chi', 'Chi-Per'],
        'Mex': ['Chi-Mex', 'Per-Mex', 'Uru-Mex'],
        'Uru': ['Uru-Per', 'Uru-Chi', 'Uru-Mex'],
        'Per': ['Uru-Per', 'Per-Mex', 'Chi-Per']
    }
};

// group of a given team
team_group = {
    'Arg': 'A',
    'Col': 'A',
    'Cos': 'A',
    'Bol': 'A',
    'Bra': 'B',
    'Ven': 'B',
    'Ecu': 'B',
    'Par': 'B',
    'Uru': 'C',
    'Per': 'C',
    'Mex': 'C',
    'Chi': 'C'
}
// teams in a given group
group_teams = {
    'A': ['Arg', 'Col', 'Cos', 'Bol'],
    'B': ['Bra', 'Ven', 'Ecu', 'Par'],
    'C': ['Uru', 'Per', 'Mex', 'Chi']
}

next_game_id_pos = {
	'qf1':['sf1','1'],
	'qf2':['sf1','2'],
	'qf3':['sf2','1'],
	'qf4':['sf2','2'],
	'sf1-l':['tf','1'],
	'sf2-l':['tf','2'],
	'sf1-w':['f','1'],
	'sf2-w':['f','2']
}

// Checks if an input value is a positive string
function isPosInt(value) {
    if (!isNaN(value) && (parseFloat(value) == parseInt(value))) {
        if (parseInt(value) >= 0) {
            return true;
        }
        return false;
    } 
    else {
            return false;
        }
}

// list of a team group matches in the form
// 'team1-team2'


function getTeamMatches(team) {
    return (matches_hash[team_group[team]])[team];
}

// splits matches of the form 'team1-team2' into
// and [team1,team2] array
function getTeamsId(match) {
    return match.split('-');
}

// calculates the match prize from two teams
// and each one goals.
// Returns 1 if the calling team wins, 2 if loses and 0 if draw 
// IMPORTANT: Calling team is the one that scored g1 goals


function getWinner(g1, g2) {
    if (g1 > g2){return 1}
    else if (g1 < g2){return 2}
    else return 0;
}

//Get goals in a form input of name 'inputName'


function getTeamGoals(inputName) {
    var goals_field = $("input[name=" + inputName + "]");
    return goals_field.val();
}

function resetTeamGoals(inputName){
    $("input[name=" + inputName + "]").val("");
}

function cleanNextMatch(match_label){
    var next = next_game_id_pos[match_label];
    $("label[for="+next[0]+"-g"+next[1]+"]").html("?");
}

// from matches of the form 'team-team' get
// actual result and if possible add result
// Result data is of the form: {"team":team, "g":0, "p":0, "e":0, "gf":0, "gc":0, "pts":0};


function calcTeamClassification(team) {
    var matches = getTeamMatches(team);
    var teamResult = {
        "team": team,
        "g": 0,
        "p": 0,
        "e": 0,
        "gf": 0,
        "gc": 0,
        "pts": 0
    };
    for (match in matches) {
        match = matches[match];
        var t1_goals = getTeamGoals(match + "-g1");
        var t2_goals = getTeamGoals(match + "-g2");
        if (isPosInt(t1_goals) && isPosInt(t2_goals)) {
            var teamsId = getTeamsId(match);
            // swap t1_goals if calling team is not the first one
            if (teamsId[0] != team) {
                var swapper = t1_goals;
                t1_goals = t2_goals;
                t2_goals = swapper;
            }
            var winResult = getWinner(t1_goals, t2_goals);
            if (winResult == 1) {
                teamResult["g"] += 1;
                teamResult["gf"] += parseInt(t1_goals);
                teamResult["gc"] += parseInt(t2_goals);
                teamResult["pts"] += 3;
            }
            else if (winResult == 2) {
                teamResult["p"] += 1;
                teamResult["gf"] += parseInt(t1_goals);
                teamResult["gc"] += parseInt(t2_goals);
            }
            else if (winResult == 0) {
                teamResult["e"] += 1;
                teamResult["gf"] += parseInt(t1_goals);
                teamResult["gc"] += parseInt(t2_goals);
                teamResult["pts"] += 1;
            }
        }else{
            if(!isPosInt(t1_goals)){
                resetTeamGoals(match + "-g1");
            }
            if(!isPosInt(t2_goals)){
                resetTeamGoals(match + "-g2");
            }
        }
    }
    return teamResult;
}
// creates a string from classification dic


function classifToString(classif) {
    //{"team":team, "g":0, "p":0, "e":0, "gf":0, "gc":0, "pts":0};
    var res = "";
    res += " team: " + classif['team'];
    res += " g: " + classif['g'];
    res += " p: " + classif['p'];
    res += " e: " + classif['e'];
    res += " gf: " + classif['gf'];
    res += " gc: " + classif['gc'];
    res += " pts: " + classif['pts'];
    return res;
}


// fetchs a goal modification and updates de results


function fetchAndUpdate(id) {

    var split_id = id.split('-');
    // team1 - team2
    var team1 = split_id[0];
    var team2 = split_id[1];
    var classif1 = calcTeamClassification(team1);
    var classif2 = calcTeamClassification(team2);
    var group = team_group[team1];
    updateClassifTable(group, classif1, classif2);
    updateAdvancingTeams(group);     


}

function updateAdvancingTeams(group){
    var stats = getTableStats(group);
    var classifUl = document.getElementById('classif-'+group);
    var childList = classifUl.getElementsByTagName("li");
    childList[0].innerHTML = stats["1"]["team"];
    childList[1].innerHTML = stats["2"]["team"];
}

function getAndUpdateThirdParty(statsA, statsB, statsC){
    var teamA = statsA['3'];
    var teamB = statsB['3'];
    var teamC = statsC['3'];
    
    var stats_list = [teamA, teamB, teamC];
    var best_thirds = reorderGivenStats(stats_list, false);
    
    // adding first third
    var classifUl = document.getElementById('classif-'+team_group[best_thirds[0]["team"]]);
    var childList = classifUl.getElementsByTagName("li");
    childList[2].innerHTML = team_long[best_thirds[0]["team"]];

    //adding second third
    classifUl = document.getElementById('classif-'+team_group[best_thirds[1]["team"]]);
    childList = classifUl.getElementsByTagName("li");
    childList[2].innerHTML = team_long[best_thirds[1]["team"]];
    
    return [best_thirds[0],best_thirds[1]];
}


// returns the classification table of a given group as
// an array of classification info such as 
// {"team":team, "g":0, "p":0, "e":0, "gf":0, "gc":0, "pts":0};
function getTableStats(group){
    var table = document.getElementById("table-"+group);
    var ttags = table.getElementsByTagName("tr");
    table_stats ={};
    // avoid the first tag (table header)
    for(var i =1; i<ttags.length; i++){
        var teamStat = ttags[i];
        var tdtags = teamStat.getElementsByTagName("td");
        var team_stats = {};
        //fill every stat
        team_stats['team']=team_acronym[tdtags[0].innerHTML];
        team_stats['g']=tdtags[1].innerHTML;
        team_stats['p']=tdtags[2].innerHTML;
        team_stats['e']=tdtags[3].innerHTML;
        team_stats['gf']=tdtags[4].innerHTML;
        team_stats['gc']=tdtags[5].innerHTML;
        team_stats['pts']=tdtags[6].innerHTML;
        table_stats[i+""]= team_stats;
    }
    return table_stats; 
}

// returns the stats for a given team in the 
// table stats dictionary returned by getTableStats(group)
/*function getTeamStatFromTableDic(team_acronym,table_stats){
    var index="";
    // the counter goes from position 1 to position 4
    for(var i=1; i<=4;i++){
        index = i+"";
        if(table_stats[index]["team"]==team_acronym){
            table_stats[index]["pos"]=index;
            return table_stats[index];
        }
    }
    return null;
}*/

function getTeamTablePos(team_acronym,table_stats){
    var index="";
    // the counter goes from position 1 to position 4
    for(var i=1; i<=4;i++){
        index = i+"";
        if(table_stats[index]["team"]==team_acronym){
            return index;
        }
    }
    return null;
}

function sumTeamStats(oldStats, resultStats){
    var newStats = {};
    newStats["team"]=oldStats["team"];
    newStats["g"]=parseInt(oldStats["g"])+parseInt(resultStats["g"]);
    newStats["e"]=parseInt(oldStats["e"])+parseInt(resultStats["p"]);
    newStats["p"]=parseInt(oldStats["p"])+parseInt(resultStats["p"]);
    newStats["gf"]=parseInt(oldStats["gf"])+parseInt(resultStats["gf"]);
    newStats["gc"]=parseInt(oldStats["gc"])+parseInt(resultStats["gc"]);
    newStats["pts"]=parseInt(oldStats["pts"])+parseInt(resultStats["pts"]);
    newStats["pos"]=oldStats["pos"];

    return newStats;
}

function updateClassifTable(group, team1Class, team2Class){
    var table_stats = getTableStats(group);
    //var team1Stats = getTeamStatFromTableDic(team1Class["team"],table_stats);
    //var team2Stats = getTeamStatFromTableDic(team2Class["team"],table_stats);
    team1Class["pos"]=getTeamTablePos(team1Class["team"],table_stats);
    team2Class["pos"]=getTeamTablePos(team2Class["team"],table_stats);
    
    //add new stats to table_stats
    table_stats[team1Class["pos"]]=team1Class;
    table_stats[team2Class["pos"]]=team2Class;
    
    var table = document.getElementById("table-"+group);
    var ttags = table.getElementsByTagName("tr");
    setHTMLTableRow(parseInt(team1Class["pos"]), ttags, team1Class);
    setHTMLTableRow(parseInt(team2Class["pos"]), ttags, team2Class);

    var ordered_list = reorderTable(group);
    setGroupTable(ordered_list,group);
}

// updates the group table according to the ordered list
// containing the stats for every team
function setGroupTable(ordered_list,group){
    var table = document.getElementById("table-"+group);
    var ttags = table.getElementsByTagName("tr");
    for(var index in ordered_list){
        setHTMLTableRow(parseInt(index)+1, ttags, ordered_list[index]);
    }
}

// sets the actual HTML row number index from the tr_element
// by the values given by teamStat
function setHTMLTableRow(index, tr_element, teamStat){
    var oldStat = tr_element[index];
    var tdtags = oldStat.getElementsByTagName("td");
    //fill every stat
    tdtags[0].innerHTML=team_long[teamStat["team"]];
    tdtags[1].innerHTML=teamStat["g"];
    tdtags[2].innerHTML=teamStat["p"];
    tdtags[3].innerHTML=teamStat["e"];
    tdtags[4].innerHTML=teamStat["gf"];
    tdtags[5].innerHTML=teamStat["gc"];
    tdtags[6].innerHTML=teamStat["pts"];   
}

//2 levels list flatten
function flatten(list){
    var flatten_list=[];
    for(var index in list){
        var inner_list = list[index];
        for(var element_index in inner_list){
            flatten_list.push(inner_list[element_index]);
        }
    }
    return flatten_list;
}

// splits in multiple lists according to
// each team points. Teams with same number 
// of points belong to the same list
function splitByPts(stat_list){
    var split_list=[];
    var change = false;
    var pt_list = [];
    var current_pts = parseInt(stat_list[0]['pts']);
    var added =0;
    for(var index in stat_list){
        var stat = stat_list[index];
        var team_points = parseInt(stat['pts']);
        // check if is necessary to create a new class of 
        // team list
        if(current_pts!==team_points){
            change=true;
        }
        
        if(change!=true){
            pt_list.push(stat);
        }
        else{
            split_list.push(pt_list);
            added+=pt_list.length;
            pt_list = new Array();
            pt_list.push(stat);
            current_pts = team_points;
            change=false;
        }
    }
    if(added<4){
        split_list.push(pt_list);
    }
    return split_list;
}

// splits in multiple lists according to
// each team goals difference. Teams with same number 
// of goals difference belong to the same list
function splitByGoals(stat_list){
    var split_list=[];
    var change = false;
    var pt_list = [];
    var current_difference = getGoalsDifference(stat_list[0]);
    var added =0;
    for(var index in stat_list){
        var stat = stat_list[index];
        var team_difference = getGoalsDifference(stat);
        // check if is necessary to create a new class of 
        // team list
        if(current_difference!==team_difference){
            change=true;
        }
        
        if(change!=true){
            pt_list.push(stat);
        }
        else{
            split_list.push(pt_list);
            added+=pt_list.length;
            pt_list = new Array();
            pt_list.push(stat);
            current_difference = team_difference;
            change=false;
        }
    }
    if(added<4){
        split_list.push(pt_list);
    }
    return split_list;
}

// splits in multiple lists according to
// each team's scored goals. Teams with same number 
// of goals scored belong to the same list
function splitByGreaterGoals(stat_list){
    var split_list=[];
    var change = false;
    var pt_list = [];
    var current_scored = parseInt(stat_list[0]['gf']);
    var added =0;
    for(var index in stat_list){
        var stat = stat_list[index];
        var team_goals = parseInt(stat['gf']);
        // check if is necessary to create a new class of 
        // team list
        if(current_scored!==team_goals){
            change=true;
        }
        
        if(change!=true){
            pt_list.push(stat);
        }
        else{
            split_list.push(pt_list);
            added+=pt_list.length;
            pt_list = new Array();
            pt_list.push(stat);
            current_scored = team_goals;
            change=false;
        }
    }
    if(added<4){
        split_list.push(pt_list);
    }
    return split_list;
}

// gets the table corresponding to the given group
// and reorders the positions
function reorderTable(group){
    var table_stats = getTableStats(group);
    var stats_list = [table_stats["1"], table_stats["2"], table_stats["3"], table_stats["4"]];
    return reorderGivenStats(stats_list, true);
}

// reorder table given table stats. draw_winner is a
// boolean indicating if a un-drawing ('desempate')
// rule must be applied
function reorderGivenStats(stats_list,draw_winner){
    var ordered_list=[];
    stats_list.sort(sortByPts);
    var split_pts_list = splitByPts(stats_list);
    for(var s_index in split_pts_list){

        split_pts_list[s_index].sort(sortByGoals);
        var sorted_goals = split_pts_list[s_index];
        var split_goals_list = splitByGoals(sorted_goals);

        // ordering by greater goals the pts and goals-diff draw
        for(var sindex in split_goals_list){
            split_goals_list[sindex].sort(sortByGreaterGoals);
            var sorted_scored_goals = split_goals_list[sindex];
            var split_scoredgoals_list = splitByGreaterGoals(sorted_scored_goals);
            
            //this will happen if two teams belong two the same list in a GreaterGoals split list
            for(var split_index in split_scoredgoals_list){
                var t_list = split_scoredgoals_list[split_index];
                if((draw_winner==true) && (t_list.length == 2)){
                    var newOrder = defineDrawWinner(t_list[0],t_list[1]);
                    split_scoredgoals_list[split_index] = newOrder;
                }
            }           
            var flat_goals = flatten(split_scoredgoals_list);
            ordered_list.push(flat_goals);
        }  
    }

    ordered_list= flatten(ordered_list);
    return ordered_list;
}

// sort by pts in descending order
function sortByPts(stat1, stat2) {
    var x = stat2['pts'];
    var y = stat1['pts'];
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
}

function getGoalsDifference(stat){
    //alert("difference: "+(parseInt(stat['gf'])-parseInt(stat['gc'])));
    return (parseInt(stat['gf'])-parseInt(stat['gc']));
}

// sort by pts in descending order
function sortByGoals(stat1, stat2) {
    var x = getGoalsDifference(stat2);
    var y = getGoalsDifference(stat1);
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
}

// sort by greater goals in descending order
function sortByGreaterGoals(stat1, stat2) {
    var x = parseInt(stat2["gf"]);
    var y = parseInt(stat1["gf"]);
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
}

// define the winner of atotal draw and returns a list
// with the same teams in the order they should appear
function defineDrawWinner(team1,team2){

    var teamOrder = [team1, team2];
    var t1acr = team1["team"];
    var t2acr = team2["team"];
    var match = t1acr+"-"+t2acr;
    
    var t1_goals = getTeamGoals(match + "-g1");
    var t2_goals = getTeamGoals(match + "-g2");
    
    // in case of wrong order assignment
    if((typeof t1_goals == "undefined") || (typeof t2_goals =="undefined")){
        match = t2acr+"-"+t1acr;
        // invert the goals order
        t1_goals = getTeamGoals(match + "-g2");
        t2_goals = getTeamGoals(match + "-g1");
    }

    if (isPosInt(t1_goals) && isPosInt(t2_goals)) {
        var t1_goals_int = parseInt(t1_goals);
        var t2_goals_int = parseInt(t2_goals);
        //alert("DRAW DEFINITION: "+team1["team"]+"-"+t1_goals+" "+team2["team"]+"-"+t2_goals);
        if(t2_goals_int > t1_goals_int){
            teamOrder = [team2,team1];
        }
    }
    return teamOrder;  
}

// determines whether the pool has been 
// filled totally or not
function isPoolFull(){
    var statsA = getTableStats('A');
    var statsB = getTableStats('B');
    var statsC = getTableStats('C'); 
    if(isTableFull(statsA) && isTableFull(statsB) && isTableFull(statsC)){
        removeThirdParty();
        var thirdParty = getAndUpdateThirdParty(statsA, statsB, statsC);
        // update the list of teams advancing to the next round
        updateAdvancingTeamsMeta(thirdParty);
        
        return true;
    }
    else{
        removeThirdParty();
    }
    return false;
}

// determines whether the pool has been 
// filled totally or not
function isFinalPoolFull(){
    var goals_field = $(".goals-field");
    var isfull = true;
    goals_field.each(function(){
        if(!(isPosInt($(this).val()))){
			isfull = false;
        }
    });
	var qf_label = $(".e1-qf");
    qf_label.each(function(){
        if($(this).html()=="?"){
			isfull = false;
        }
    });
	var qf_label = $(".e2-qf");
    qf_label.each(function(){
        if($(this).html()=="?"){
			isfull = false;
        }
    });
	qf_label = $(".e1");
    qf_label.each(function(){
        if($(this).html()=="?"){
			isfull = false;
        }
    });
	qf_label = $(".e2");
    qf_label.each(function(){
        if($(this).html()=="?"){
			isfull = false;
        }
    });

    return isfull;
}

// determines whether the pool has been 
// filled totally or not
function setAllResultsData(){
    var goals_field = $(".goals-field");
    
    // get all qf goals
    var count=0;
    var pair=0;
    var total="";
    var construct ="";
    goals_field.each(function(){
        if(count==8) return false;
        if(pair==0){
            construct="[";
            construct+="'qf-"+$(this).attr("name")+"'";
            construct+=",";
            construct+="'"+$(this).val()+"'";
            construct+=",";
        }
        if(pair==1){
            construct+="'qf-"+$(this).attr("name")+"'";
            construct+=",";
            construct+="'"+$(this).val()+"'";
            construct+="]";
            if(total==""){
              total+=construct;   
            }else{
            total+=","+construct;
            }
     }	
        pair+=1;
        if(pair==2){
            pair=0;
        }
        count+=1;        
    });       
    construct="[";
    var gname = "'sf-"+team_acronym[$("label[for=sf1-g1]").html()]+
        "-"+team_acronym[$("label[for=sf1-g2]").html()]+"-";
    construct+=gname+"g1'"+",";
    construct+="'"+$("input[name=sf1-g1]").val()+"',";
    construct+=gname+"g2'"+", ";
    construct+="'"+$("input[name=sf1-g2]").val()+"']";
    total+=","+construct+", ";
    
    construct="[";
    var gname = "'sf-"+team_acronym[$("label[for=sf2-g1]").html()]+
    "-"+team_acronym[$("label[for=sf2-g2]").html()]+"-";
    construct+=gname+"g1'"+",";
    construct+="'"+$("input[name=sf2-g1]").val()+"',";
    construct+=gname+"g2'"+", ";
    construct+="'"+$("input[name=sf2-g2]").val()+"']";
    total+=construct+", ";
    
    construct="[";
    var gname = "'tf-"+team_acronym[$("label[for=tf-g1]").html()]+
    "-"+team_acronym[$("label[for=tf-g2]").html()]+"-";
    construct+=gname+"g1'"+",";
    construct+="'"+$("input[name=tf-g1]").val()+"',";
    construct+=gname+"g2'"+", ";
    construct+="'"+$("input[name=tf-g2]").val()+"']";
    total+=construct+", ";
    
    construct="[";
    var gname = "'f-"+team_acronym[$("label[for=f-g1]").html()]+
    "-"+team_acronym[$("label[for=f-g2]").html()]+"-";
    construct+=gname+"g1'"+",";
    construct+="'"+$("input[name=f-g1]").val()+"',";
    construct+=gname+"g2'"+", ";
    construct+="'"+$("input[name=f-g2]").val()+"']";
    total+=construct;

    
    var finalRes = "["+total+"]";
    alert(finalRes);
    //var cable = "[['qf1-Arg-Col-g1', '2', 'qf1-Arg-Col-g2', '2'], ['qf2-Uru-Chi-g1', '3', 'qf2-Uru-Chi-g2', '0'], ['qf3-Bol-Cos-g1', '0', 'qf3-Bol-Cos-g2', '4'], ['qf4-Ven-Ecu-g1', '6', 'qf4-Ven-Ecu-g2', '2'], ['sf1-Ven-Bol-g1', '2', 'sf1-Ven-Bol-g2', '1'], ['sf2-Col-Bol-g1', '0', 'sf2-Col-Bol-g2', '1'], ['tf-Ecu-Chi-g1', '1', 'tf-Ecu-Chi-g2', '4'], ['f-Ven-Bra-g1', '3', 'f-Ven-Bra-g2', '2']]";
    $("input[name=second-round-matches]").val(finalRes);
    //alert(finalRes);
    //alert( $("input[name=second-round-matches]").val());
    
}

// Updates the advancing teams hidden field. The best third
// are passed to optimize updating speed
function updateAdvancingTeamsMeta(thirdParty){
    //[['qf1', 'Arg-Col'], ['qf2', 'Uru-Chi'], ['qf3', 'Bol-Cos'], ['qf4', 'Ven-Ecu']]"
    var qf_matches ="[";
  
    // group Fixtures
    var classifA = getTableStats('A');
    //firstA vs 1st Best third
    qf_matches+=getQfMatchAsString("1", classifA["1"]["team"], thirdParty[0]["team"]);
    qf_matches+=",";
    
    //second A vs Second Group C
    var classifC = getTableStats('C');
    qf_matches+=getQfMatchAsString("2", classifA["2"]["team"], classifC["2"]["team"]);
    qf_matches+=",";
    //1st B vs Snd best third
    var classifB = getTableStats('B');
    qf_matches+=getQfMatchAsString("3", classifB["1"]["team"], thirdParty[1]["team"]);
    qf_matches+=",";
    
    //1st C vs Snd B
    qf_matches+=getQfMatchAsString("3", classifC["1"]["team"], classifB["2"]["team"]);
    qf_matches+="]";
    
    $("input[name=first-round-winners]").val(qf_matches);
}

function updateFinalTeamsMeta(){
    
}

function getQfMatchAsString(number, team1, team2){
    var qf_match ="[";
    qf_match+="'qf"+number+"',";
    qf_match+="'"+team1+"-"+team2+"']";
    return qf_match;
}


function removeThirdParty(){
        
    var groups = ['A','B','C'];  
    for(gindex in groups){
        var group = groups[gindex];
        // adding first third
        var classifUl = document.getElementById('classif-'+group);
        var childList = classifUl.getElementsByTagName("li");
        childList[2].innerHTML = '';
    }

}

// true if every sum of win, lost and draw games for every team  in the 
// given stats equals 3
function isTableFull(table_stats){
    for(var i=1; i<4; i++){
        var stat = table_stats[i];
        if((parseInt(stat["g"])+parseInt(stat["p"])+parseInt(stat["e"]))!=3){
            return false;
        }
    }
    return true;
}

/*
function fetchAllResults(){
   
   var teams= ['Arg','Col','Cos','Bol','Bra','Ven','Ecu','Par','Uru','Per','Mex','Chi'];
   setted = {};
   var matches={};
   for(team in teams){
       matches = getTeamMatches(team);
       for(match in matches){
           if(setted[match]) continue;
            else{
                setted[match]=true;
                
                $('#'+match).change(function() {
                    fetchAndUpdate(match+"-g1");
                })
    
                 $('#'+match).change(function() {
                    fetchAndUpdate(match+"-g2");
                }) 
            }
        }
       
    }
}*/

function statListToString(stat_list){
    var res="";
    res+="team: "+stat_list["team"]+" ";
    res+="g: "+stat_list["g"]+" ";
    res+="e: "+stat_list["e"]+" ";
    res+="p: "+stat_list["p"]+" ";
    res+="gf: "+stat_list["gf"]+" ";
    res+="gc: "+stat_list["gc"]+" ";
    res+="pts: "+stat_list["pts"]+" ";
    return res;
    
}

function fetchAllResults(){
	
$('#Arg-Bol-g1').change(function() {fetchAndUpdate('Arg-Bol-g1');})
$('#Arg-Bol-g2').change(function() {fetchAndUpdate('Arg-Bol-g2');})
$('#Arg-Cos-g1').change(function() {fetchAndUpdate('Arg-Cos-g1');})
$('#Arg-Cos-g2').change(function() {fetchAndUpdate('Arg-Cos-g2');})
$('#Arg-Col-g1').change(function() {fetchAndUpdate('Arg-Col-g1');})
$('#Arg-Col-g2').change(function() {fetchAndUpdate('Arg-Col-g2');})
$('#Col-Cos-g1').change(function() {fetchAndUpdate('Col-Cos-g1');})
$('#Col-Cos-g2').change(function() {fetchAndUpdate('Col-Cos-g2');})
$('#Col-Bol-g1').change(function() {fetchAndUpdate('Col-Bol-g1');})
$('#Col-Bol-g2').change(function() {fetchAndUpdate('Col-Bol-g2');})
$('#Bol-Cos-g1').change(function() {fetchAndUpdate('Bol-Cos-g1');})
$('#Bol-Cos-g2').change(function() {fetchAndUpdate('Bol-Cos-g2');})
$('#Bra-Ven-g1').change(function() {fetchAndUpdate('Bra-Ven-g1');})
$('#Bra-Ven-g2').change(function() {fetchAndUpdate('Bra-Ven-g2');})
$('#Bra-Par-g1').change(function() {fetchAndUpdate('Bra-Par-g1');})
$('#Bra-Par-g2').change(function() {fetchAndUpdate('Bra-Par-g2');})
$('#Bra-Ecu-g1').change(function() {fetchAndUpdate('Bra-Ecu-g1');})
$('#Bra-Ecu-g2').change(function() {fetchAndUpdate('Bra-Ecu-g2');})
$('#Ven-Ecu-g1').change(function() {fetchAndUpdate('Ven-Ecu-g1');})
$('#Ven-Ecu-g2').change(function() {fetchAndUpdate('Ven-Ecu-g2');})
$('#Par-Ven-g1').change(function() {fetchAndUpdate('Par-Ven-g1');})
$('#Par-Ven-g2').change(function() {fetchAndUpdate('Par-Ven-g2');})
$('#Par-Ecu-g1').change(function() {fetchAndUpdate('Par-Ecu-g1');})
$('#Par-Ecu-g2').change(function() {fetchAndUpdate('Par-Ecu-g2');})
$('#Uru-Per-g1').change(function() {fetchAndUpdate('Uru-Per-g1');})
$('#Uru-Per-g2').change(function() {fetchAndUpdate('Uru-Per-g2');})
$('#Chi-Mex-g1').change(function() {fetchAndUpdate('Chi-Mex-g1');})
$('#Chi-Mex-g2').change(function() {fetchAndUpdate('Chi-Mex-g2');})
$('#Uru-Chi-g1').change(function() {fetchAndUpdate('Uru-Chi-g1');})
$('#Uru-Chi-g2').change(function() {fetchAndUpdate('Uru-Chi-g2');})
$('#Per-Mex-g1').change(function() {fetchAndUpdate('Per-Mex-g1');})
$('#Per-Mex-g2').change(function() {fetchAndUpdate('Per-Mex-g2');})
$('#Uru-Mex-g1').change(function() {fetchAndUpdate('Uru-Mex-g1');})
$('#Uru-Mex-g2').change(function() {fetchAndUpdate('Uru-Mex-g2');})
$('#Chi-Per-g1').change(function() {fetchAndUpdate('Chi-Per-g1');})
$('#Chi-Per-g2').change(function() {fetchAndUpdate('Chi-Per-g2');})
}

function loadPrevResults(){
    fetchAndUpdate('Arg-Bol-g1')
    fetchAndUpdate('Arg-Bol-g2');
    fetchAndUpdate('Arg-Cos-g1');
    fetchAndUpdate('Arg-Cos-g2');
    fetchAndUpdate('Arg-Col-g1');
    fetchAndUpdate('Arg-Col-g2');
    fetchAndUpdate('Col-Cos-g1');
    fetchAndUpdate('Col-Cos-g2');
    fetchAndUpdate('Col-Bol-g1');
    fetchAndUpdate('Col-Bol-g2');
    fetchAndUpdate('Bol-Cos-g1');
    fetchAndUpdate('Bol-Cos-g2');
    fetchAndUpdate('Bra-Ven-g1');
    fetchAndUpdate('Bra-Ven-g2');
    fetchAndUpdate('Bra-Par-g1');
    fetchAndUpdate('Bra-Par-g2');
    fetchAndUpdate('Bra-Ecu-g1');
    fetchAndUpdate('Bra-Ecu-g2');
    fetchAndUpdate('Ven-Ecu-g1');
    fetchAndUpdate('Ven-Ecu-g2');
    fetchAndUpdate('Par-Ven-g1');
    fetchAndUpdate('Par-Ven-g2');
    fetchAndUpdate('Par-Ecu-g1');
    fetchAndUpdate('Par-Ecu-g2');
    fetchAndUpdate('Uru-Per-g1');
    fetchAndUpdate('Uru-Per-g2');
    fetchAndUpdate('Chi-Mex-g1');
    fetchAndUpdate('Chi-Mex-g2');
    fetchAndUpdate('Uru-Chi-g1');
    fetchAndUpdate('Uru-Chi-g2');
    fetchAndUpdate('Per-Mex-g1');
    fetchAndUpdate('Per-Mex-g2');
    fetchAndUpdate('Uru-Mex-g1');
    fetchAndUpdate('Uru-Mex-g2');
    fetchAndUpdate('Chi-Per-g1');
    fetchAndUpdate('Chi-Per-g2');
}

function loadQuinEvents(){
    loadPrevResults();
	fetchAllResults();
    
    $('#create-step1').submit(function(event){
        if(!isPoolFull()){
            alert("Pooll is not full");
            event.preventDefault();
            return false;
        }
		// must provide pool name
		else{
			if($("input[name=football-pool-name]").val()==""){
				alert("Provide Name");
				event.preventDefault();
				return false;
			}
		};
        return true;
    });    
}

function loadFinalRoundEvents(){
    fetchFinalRoundEvents();
            
    $('#create-step2').submit(function(event){

        if(!isFinalPoolFull()){
            alert("Pooll is not full");
            event.preventDefault();
            return false;
        }
        //set hidden data
        setAllResultsData();
        
        return true;
    });    
	
	
}

function fetchFinalRoundEvents(){

    var qf_games = getFinalRoundMatches("e1-qf");
	var match_name;
	var match_id;
	var match_element;
	for(var index_qf in qf_games){
		match_name=(qf_games[index_qf]).split('-');
		match_id = match_name[0]+"-"+match_name[1];
		$("#"+match_id+"-g1").change(function(){
			fetchQfGame($(this).attr('id'), $(this));
		});
		$("#"+match_id+"-g2").change(function(){
			fetchQfGame($(this).attr('id'),$(this));	
		});
	}
}

function fetchQfGame(qfmatch, input_element){

	var match = qfmatch.split('-');
	var t1_goals = getTeamGoals(match[0]+"-"+match[1]+"-g1");
	var t2_goals = getTeamGoals(match[0]+"-"+match[1]+"-g2");
	
	if (isPosInt(t1_goals) && isPosInt(t2_goals)) {
        var t1_goals_int = parseInt(t1_goals);
        var t2_goals_int = parseInt(t2_goals);

		var winner = getWinner(t1_goals_int, t2_goals_int);
		var parent;
         if(winner==1){
			parent = input_element.parent();
			setNextGameTeam(parent.attr("id"), match[0]);
		}
		else if(winner==2){
			parent = input_element.parent();
			setNextGameTeam(parent.attr("id"), match[1]);
		}
		else if(winner==0){
			alert("El partido no puede quedar empatado");
			resetTeamGoals(match[0]+"-"+match[1]+"-g1");
			resetTeamGoals(match[0]+"-"+match[1]+"-g2");
			cleanNextMatch(parent.attr("id"));
		}
    }else{
        parent = input_element.parent();
        if(!isPosInt(t1_goals)){
            resetTeamGoals(match[0]+"-"+match[1]+"-g1");
            cleanNextMatch(parent.attr("id"));
        }
        if(!isPosInt(t2_goals)){
            resetTeamGoals(match[0]+"-"+match[1]+"-g2");
            cleanNextMatch(parent.attr("id"));          
        }
    }
}

function setNextGameTeam(prev_game_id, team_name){
	var next_game = next_game_id_pos[prev_game_id];
	var game_level= next_game[0];
	var team_pos = next_game[1];
	
	if(team_pos =='1'){
		$("label[for="+game_level+"-g1"+"]").html(team_long[team_name]);
		$("input[name="+game_level+"-g1]").change(function(){
			fetchFRGame($(this));	
		});
	}
	else if(team_pos =='2'){
		$("label[for="+game_level+"-g2"+"]").html(team_long[team_name]);
		$("input[name="+game_level+"-g2]").change(function(){
			fetchFRGame($(this));	
		});
	}
}

function fetchFRGame(input_element){
	var split_name = input_element.attr("name").split('-');
	var round = split_name[0];
	var calling_team_g = split_name[1];
	var t1_goals = getTeamGoals(round+"-g1");
	var t2_goals = getTeamGoals(round+"-g2");
	
	if (isPosInt(t1_goals) && isPosInt(t2_goals)) {
        var t1_goals_int = parseInt(t1_goals);
        var t2_goals_int = parseInt(t2_goals);

		var winner = getWinner(t1_goals_int, t2_goals_int);
		var parent;
         if(winner==1){   
			setNextGameTeam(round+"-w", team_acronym[$("label[for="+round+"-g1"+"]").html()]);
                        setNextGameTeam(round+"-l", team_acronym[$("label[for="+round+"-g2"+"]").html()]);
		}
		else if(winner==2){
			setNextGameTeam(round+"-w", team_acronym[$("label[for="+round+"-g2"+"]").html()]);
                        setNextGameTeam(round+"-l", team_acronym[$("label[for="+round+"-g1"+"]").html()]);
		}
		else if(winner==0){
			resetTeamGoals(round+"-g1");
			resetTeamGoals(round+"-g2");
			alert("El partido no puede quedar empatado");
		}
    }else{parent = input_element.parent();
            if(!isPosInt(t1_goals)){
                resetTeamGoals(round+"-g1");
                cleanNextMatch(parent.attr("id")); 
                
            }
            if(!isPosInt(t2_goals)){
                resetTeamGoals(round+"-g2");
                cleanNextMatch(parent.attr("id")); 
            }
        }
}

function getFinalRoundMatches(className){
	var games = $("."+className);
	var games_id = [];
	games.each(function(index) {
	    games_id.push($(this).attr('for'));
	  });
	return games_id;
}







