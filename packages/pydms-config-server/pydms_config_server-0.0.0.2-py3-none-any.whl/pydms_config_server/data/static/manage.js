
let cfg={
    urls:{
        config:'/config'
    }
}
const get_config=()=>{
    let data=$.get({
        url:cfg.urls.config,
        async:false,
    }).responseJSON;
    return data;
}



class App{
    constructor(){
        get_config();
    }

}

let app=new App();