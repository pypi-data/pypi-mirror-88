
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
const post_config=(data)=>{
  let res=$.post({
    url:cfg.urls.config,
    data:JSON.stringify(data),
    contentType:'appication/json',
    async:false
  }).responseJSON;
  return res;
}
const mergeData=(data,values)=>{
  Object.keys(values).map(key=>{
    data[key].value=values[key];
  });
  return data;
}
$(()=>{

  let data=get_config();
$('#jsonform').jsonForm({
        schema: data,
        onSubmit: function (errors, values) {
          if (errors){
            alertify.error('error occurred !');
          }else{
            data=mergeData(data,values);
            console.log(data);
            let res=post_config(data);
            if(res.success){
              alertify.success(res.message);
            }else{
              alertify.error(res.message);
            }
          }
        }
      });
})
