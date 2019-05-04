class IntervalTimer{
    constructor(event_interval=1000){
        this.start_time=Date.now();
        this.run=false;
        this.event_interval=event_interval;
        this.on_event=undefined;
    }
    start(){
        //this.start_time=Date.now();
        // var that=this;
        // this.event= setTimeout(that.do_event,2000);
        // this.event=setTimeout(this.do_event.bind(this),2000);
        this.run=true;
        this.do_event();
    }
    stop(){
        this.run=false;
    }
    time(){
        return Math.round((Date.now()-this.start_time)/1000);
    }
    time_string(){
        var time=this.time();
        var h=Math.floor(time/3600);
        var m=Math.floor((time-h*3600)/60);
        var s=time-h*3600-m*60;
        h=""+h;
        h=h.padStart(2,'0');
        m=""+m;
        m=m.padStart(2,'0');
        s=""+s;
        s=s.padStart(2,'0');
        return (h+":"+m+":"+s)
    }
    do_event(){
        if (!this.run){
            return;
        }
        // console.log(this.time());
        // console.log("hello")
        if (this.on_event){
            this.on_event();
        }
        this.event=setTimeout(this.do_event.bind(this),this.event_interval);
    }
}

// Use example:
// t=new IntervalTimer;

// function f(){
//     console.log(t.time());
// }
// t.on_event=function(){console.log(t.time())};

// t.start();
