document.writeln("<script src='\/js\/ajax.js'><\/script>");
function checkInput(){
    var s = document.getElementById("s_key").value ;
    if(s.length < 2 ){ alert("请输入两个或以上中文"); return false; }
    if(s == "输入书名或作者，可少字不要错字"){ alert("请输入搜索关键词"); return false; }
}
function showlogin(){//顶部登录框判断是否登录
    doAjax("/ajax.php", "showlogin=1", "showlogin2", "GET", 0);
}
function showlogin2(t){//顶部登录框判断是否登录
    var t = t.replace(/\s/g,'');
    var login_top = document.getElementById("login_top");
    if(t != "nologin"){
        login_top.innerHTML =
            "<a>"+t+"</a><a href='/mybook.php' >我的书架</a><a href=\"javascript:;\" onclick=\"logout()\" >退出</a>";
    }
}
function login(){//开启登录
    uname = document.getElementById("username").value;
    upass = document.getElementById("userpass").value;

    doAjax("/login_go.php", "chname=" + uname + "&chpass=" + upass, "go_login", "POST", 0);
}
function go_login(t){
    //alert(decodeURIComponent(t));
    doAjax("/ajax.php", "is_login=1", "is_login", "GET", 0);
}

function is_login(t){
    var t = t.replace(/\s/g,'');
    if(t == "right"){
        var urlarray= new Array(); //定义一数组
        urlarray = document.URL.split("?url="); //字符分割
        url = urlarray[1];
        document.getElementById("logintips").innerHTML = "<a class='anjian'>登录成功！</a>";
        if(url){
            url = url.replace(/\%2F/g,"/");
            url = url.replace(/\%3A/g,":");
            url = url.replace(/\%23/g,"");
            url = url.replace(/\%3F/g,"?");
            url = url.replace(/\%3D/g,"=");
            url = url.replace(/\%26/g,"&");
            window.location.href = url;
        }
        else{
            window.location.href = "/";
        }
    }
    else{
        alert("帐号或密码错误，登录失败！"); return false;
    }
}
//退出登录
function logout(){
    doAjax("/logout.php", "t=1", "logout2", "GET", 0);
}
function logout2(){
    window.location.href = "/";
}
function register(){
    uname = document.getElementById("regname").value;
    upass = document.getElementById("regpass").value;
    uemail = document.getElementById("regemail").value;
    doAjax("/register_go.php", "uname=" + uname + "&upass=" + upass + "&uemail=" + uemail, "go_register", "POST", 0);
}
function go_register(t){
    var t = t.replace(/\s/g,'');
    var tips = document.getElementById("logintips");
    if(t == "nodata"){
        alert("以上信息都必须输入"); return false;
    }
    if(t == "bigname"){
        alert("用户名太长！10个中问或者30个英文以内！"); return false;
    }
    if(t == "bigpass"){
        alert("密码太长！16位以内！"); return false;
    }
    if(t == "bigemail"){
        alert("邮箱太长！"); return false;
    }
    if(t == "emailerror"){
        alert("邮箱格式错误！"); return false;
    }
    if(t == "havename"){
        alert("用户名已被注册！"); return false;
    }
    if(t == "haveemial"){
        alert("邮箱已被注册！"); return false;
    }
    if(t == "yesregister"){
        document.getElementById("success").innerHTML ="<a class='anjian' >注册成功并已经登录！</a>";
        window.location.href = "/";
    }
}
function case_del(aid,uid){
    //alert(aid+"+"+uid);
    doAjax("/ajax.php", "aid=" + aid +"&uid=" + uid, "case_del2", "POST", 0);
    document.getElementById("" + aid).innerHTML = "<tr><td style='height:30px;line-height:30px;'><font color=red>删除中，请稍后...</font></td></tr>";
}
function case_del2(t){
    var t = t.replace(/\s/g,'');
    //alert(t);
    if(t != ""){
        table = document.getElementById("" + t);
       // table.style.backgroundColor = "#D3FEDA";

        table.innerHTML = "<font color=red>已从书架删除！</font>";

    }
}
function shuqian(aid,cid,urlchapter){
    //alert("shuqian");
    doAjax("/ajax.php", "addmark=1&urlchapter="+urlchapter+"&aid=" + aid + "&cid=" + cid, "shuqian2", "GET", 0);
}
function shuqian2(t){
    var t = t.replace(/\s/g,'');
    //alert(t);
    var a = t.split("|");
    if(a[0]==1){
        document.getElementById("pt_prev").innerHTML = "<font color=red>已存书签</font>";
        document.getElementById("pt_prev1").innerHTML = "<font color=red>已存书签</font>";
    }
    if(a[0]==0){
        window.location.href = "/login.php?url="+a[1];
    }
}
function shujia(aid,urlinfo){
    //alert("shujia");
    doAjax("/ajax.php", "addbookcase=1&urlinfo="+urlinfo+"&aid=" + aid, "shujia2", "GET", 0);
}
function shujia2(t){
    var t = t.replace(/\s/g,'');
    var divshujia = document.getElementById("shujia");
    var url = window.location.href
    var a = t.split("|");
    if(a[0]==1){
        divshujia.innerHTML = "<a>已加入书架！</a>";
    }
    if(a[0]==0){
        window.location.href = "/login.php?url="+url;
    }
}
function tuijian(aid) {
    doAjax("/ajax.php", "tuijian=1&aid=" + aid, "tuijian2", "GET", 0);
}
function tuijian2(t){
    if(t==1){
    document.getElementById("tuijian").innerHTML = "<a>已推荐！</a>";
    }
}
function show_search(){

    var type = document.getElementById("type");
    var searchType = document.getElementById("searchType");
    if(type.innerHTML == "书名"){
        type.innerHTML = "作者";
        searchType.value = "author";
        //alert(searchType.value);
    }
    else{
        type.innerHTML = "书名";
        searchType.value = "articlename";
    }
}

//内容页用户设置
function deng(){
    if(localStorage.getItem('ccc') == "hei"){
        dengguang("bai");
        localStorage.setItem('ccc','bai');
    }
    else{
        dengguang("hei");
        localStorage.setItem('ccc','hei');
    }
}
function dengguang(yanse){
    if(yanse=="hei"){
        document.getElementById("neirong").className="yanse2";
        document.getElementById("deng").innerHTML = "开灯";
        document.getElementById("moshi").style.background="#121212"
    }
    else if(yanse=="bai"){
        document.getElementById("neirong").className="yanse1";
        document.getElementById("deng").innerHTML = "关灯";
        document.getElementById("moshi").style.background="#d8e3e7"
    }
}

function ziti() {
    if(localStorage.getItem('bbb')==null){
        var zi="xiao";
    }
    else{
        var zi=localStorage.getItem('bbb');
    }
    if(zi=="xiao"){
        document.getElementById("ziti").innerHTML="字号：中";
        changeziti("zhong")
        localStorage.setItem('bbb','zhong');
    }
    else if(zi=="zhong"){
        document.getElementById("ziti").innerHTML="字号：大";
        changeziti("da")
        localStorage.setItem('bbb','da');
    }
    else if(zi=="da"){
        document.getElementById("ziti").innerHTML="字号：小";
        changeziti("xiao")
        localStorage.setItem('bbb','xiao');
    }
}
function changeziti(type){
    if(type=="xiao"){
        document.getElementById("txt").style.fontSize="22px"
        document.getElementById("txt").style.lineHeight="50px"
        document.getElementById("ziti").innerHTML="字号：小";
    }
    else if(type=="zhong"){
        document.getElementById("txt").style.fontSize="26px"
        document.getElementById("txt").style.lineHeight="65px"
        document.getElementById("ziti").innerHTML="字号：中";
    }
    else if(type=="da"){
        document.getElementById("txt").style.fontSize="30px"
        document.getElementById("txt").style.lineHeight="80px"
        document.getElementById("ziti").innerHTML="字号：大";
    }
}
function gaibain(){
    var bbb = localStorage.getItem('bbb');
    var ccc = localStorage.getItem('ccc');
    changeziti(bbb);
    dengguang(ccc);
}

function xiaoshi(){
    if(document.getElementById("xiaoshi").className=="jilu1"){
        document.getElementById("xiaoshi").className="jilu"
    }
     else {
        document.getElementById("xiaoshi").className="jilu1"
    }
}

function tijiao(url){
    var leixing=document.getElementById("cuowu").value;
    var yanzhengma=document.getElementById("yanzhengma").value;
    doAjax("/ajax.php", "tijiao=" + yanzhengma + "&url=" + url +"&leixing=" + leixing , "tijiao2", "GET", 0);
}
function tijiao2(t){
    if(t==1){
        alert("提交成功！");
        document.getElementById("zhezhao").className="zhezhao";
    }
    else {
        alert("验证码错误！"); return false;
    }
}
function yanzheng(url) {
    document.getElementById("zhezhao").className="zhezhao1";
    document.getElementById("shengcheng").innerHTML="<img src=\"/yanzheng.php\">"
}
function guanbi() {
    document.getElementById("zhezhao").className="zhezhao";
}
