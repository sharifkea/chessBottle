const img_location = {board:"static/img/Chess_Board_2.png", WK:"static/img/Chess_wk.svg.png", WQ:"static/img/Chess_wq.svg.png", 
WP:"static/img/Chess_wp.svg.png", WR:"static/img/Chess_wr.svg.png", WB:"static/img/Chess_wb.svg.png", WN:"static/img/Chess_wn.svg.png", 
ZK:"static/img/Chess_zk.svg.png", ZQ:"static/img/Chess_zq.svg.png", ZP:"static/img/Chess_zp.svg.png", ZR:"static/img/Chess_zr.svg.png", 
ZB:"static/img/Chess_zb.svg.png", ZN:"static/img/Chess_zn.svg.png"}; 
var myBoard=[], myBId=[], count=0, arr=[],turn='',ext='', allcast=[],get_move='',move_count=0,white_moves=[],
black_moves=[],captured=[],en_passant=0,ret=[],valid=true;


$(document).ready(function() {
   
    let top=60, left=60, width=600;
    console.log(img_location.WK);
    insertIcon(img_location.board,"BD",top, left, width,"It is the Board")
    fetchData(top, left,{"first":true,"data":"false"});
    
    $("#input_form").on("submit", function(e) {
        e.preventDefault();
        get_move=$("#input_get").val()
        if(!valid)valid=true;
        let ret=[]
        ret.push(arr);
        ret.push(allcast);
        ret.push(turn);
        ret.push(get_move);
        ret.push(move_count);
        ret.push(white_moves);
        ret.push(black_moves);
        ret.push(captured);
        ret.push(en_passant);
        ret.push(ext);
        ret.push(valid);
        let newdata=JSON.stringify(ret);
        fetchData(top, left,{"first":false,"data":newdata});
    });
    
});


function insertIcon(newImg,setId,t,l,w,name){
    console.log(newImg);
    console.log(setId);
    console.log(t,l)
    const aa = $('<img src="'+newImg+'" id="'+setId+'" name="'+name+'"/>');
    let display = document.getElementById("board");
    aa.appendTo($(display));
           $("img#"+setId)
                .css({
                  "position":"absolute",
                    "top":t,
                    "left":l,
                    "width": w                 
                });
    console.log(setId);
    let ael = document.getElementById(setId);
    //ael.addEventListener("mousedown", initialClick, false);
    myBId[count]=setId;
    count++;
    console.log(myBId);
}
function removeImage(imageId) {
    var image = document.getElementById(imageId);
    if (image) {
        image.remove();
    } else {
        console.log("Image not found.");
    }
}

async function fetchData(top, left, mydata) {
    console.log(mydata.first)
    //try {
        // Use jQuery's $.ajax() method to make the GET request
        await $.ajax({
            url: 'http://127.0.0.1:5000/first',
            type: 'POST',
            data: JSON.stringify(mydata), // Convert JavaScript object to JSON string
            contentType: 'application/json', // Set content type to JSON
            success: function(response) {
                console.log(response); // No need to parse JSON, jQuery handles it automatically
                let input=JSON.parse(response);
                arr=input[0], allcast=input[1],turn=input[2],get_move=input[3],move_count=input[4],white_moves=input[5],
                black_moves=input[6],captured=input[7],en_passant=input[8],ext=input[9],valid=input[10];
                for (let x in myBId){
                    if(x!=0){
                        removeImage(myBId[x]);

                    }
                }
                count=1;
                top=top+10
                left=left+10
                let z=0;
                for (let x in arr) {
                    for (let y in arr[x]) {
                        myBoard[z]=arr[x][y]
                        if(arr[x][y]){
                            let sub=arr[x][y].substr(0, 2)
                            console.log(img_location[sub])
                            insertIcon(img_location[sub],arr[x][y],top+525-(75*x),left+(y*75),60,"It is the "+arr[x][y])
                        }
                        z++
                    }
                }
                if (!valid){
                    if(ext!='') alert(ext);
                    else alert("Invalied Input");
                }
                else{
                    if(captured[0]){
                        for (let x = 1; x < captured.length; x++){
                            console.log(captured[x])
                            let sub=captured[x].substr(0, 2)
                            insertIcon(img_location[sub],captured[x],(25+60*x),930,60,"It is the "+captured[x])
                        }
                    }
                    
                    let mc = Math.floor(move_count / 2); // Get the integer division
                    let r = move_count % 2;
                    let y=0;
                    if(move_count){
                        var ex=0;
                        $('#movesTable tbody').empty();
                        var tbody = $('#movesTable tbody');
                        var tr = '';
                        if(move_count==2){tr = `<tr>
                            <td>1</td>
                            <td>${white_moves[0]}</td>
                            <td></td>
                            </tr>
                            `;
                            tbody.append(tr);
                        }
                        else if(mc){
                            if(!r){ y=mc-1;ex=1;}
                            else  y=mc;
                            for (let x = 0; x < y; x++) {
                                
                                tr =`<tr>
                                <td>${x+1}</td>
                                <td>${white_moves[x]}</td>
                                <td>${black_moves[x]}</td>
                                </tr>
                                `;
                                tbody.append(tr);
                            }    
                        }
                        if(ex){tr = `<tr>
                            <td>${mc}</td>
                            <td>${white_moves[mc-1]}</td>
                            <td></td>
                            </tr>
                            `;
                            tbody.append(tr);
                        }
                        

                    }
                    
                    if(r){
                        //<label id="input_lable_id">'White: Enter move number 1: ':</label>
                        console.log(move_count)
                        document.getElementById('input_lable_id').innerHTML = 'White: Enter move number '+(mc+1)+': ';
                    }
                    else{
                        document.getElementById('input_lable_id').innerHTML = 'Black: Enter move number '+mc+': ';
                    }
                    
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        
        });
        
    
}
