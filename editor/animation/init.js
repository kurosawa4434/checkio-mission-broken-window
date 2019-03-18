//Dont change it
requirejs(['ext_editor_io', 'jquery_190', 'raphael_210'],
    function (extIO, $, TableComponent) {
        function brokenWindowCanvas(dom, input, data) {

            if (! data) {
                return
            }

            $(dom.parentNode).find(".answer").remove()
            
            const result = data.ext.result
            const output = data.out
            const error = data.ext.result_addon[1]
            const height = data.ext.explanation

            if (! result && error !== 'Fail') {
                return
            }

            let top = []
            let bottom = []

            output[0].forEach(i=>{
                const rev = input[i].slice().reverse()
                top.push(rev)
            })
            output[1].forEach(i=>{
                bottom.push(input[i])
            })

            function assemble_fragments(fragments) {
                let assembly = []
                fragments.forEach(f=>{
                    if (assembly.length > 0
                        && assembly[assembly.length-1] === f[0]) {
                        assembly.pop()
                    }
                    assembly = assembly.concat(f)
                })
                return assembly
            }

            const top_order = assemble_fragments(top)
            const bottom_order = assemble_fragments(bottom)
            const [top_len, bottom_len]
                = [top_order.length, bottom_order.length]

            let top_width = 0
            let bottom_width = 0
            top.forEach(t=>{
                top_width += t.length-1
            })
            bottom.forEach(b=>{
                bottom_width += b.length-1
            })
            const width = Math.max(top_width, bottom_width)

            let heights = []
            for (let j = 0; j < Math.min(top_len, bottom_len); j += 1) {
                heights.push(top_order[j]+bottom_order[j])
            }

            //const height =  Math.max(...heights)

            const attr = {
                mountain: {
                    content: {
                        'stroke': '#F0801A',
                        'stroke-width': 0.5/(width/20)+'px',
                        'stroke-linejoin': 'round',
                        'stroke-linecap': 'round',
                        'fill': '#FABA00',
                    }
                },
                flood: {
                    after: {
                        'fill': 'skyblue',
                        'stroke-width': 0.5/(width/20)+'px',
                        'stroke-linejoin': 'round',
                        'stroke-linecap': 'round',
                        'stroke': '#2080B8',
                    }
                },
            }

            /*----------------------------------------------*
             *
             * paper
             *
             *----------------------------------------------*/
            let max_width = 350
            const os = 10
            const SIZE = (max_width - os*2) / width
            max_width = Math.min(350, SIZE*width+os*2)
            const paper = Raphael(dom, max_width, SIZE*height+os*2, 0, 0)

            /*----------------------------------------------*
             *
             * draw
             *
             *----------------------------------------------*/
            let [fx, fy] = [0, 0]

            top.forEach(f=>{
                let path = ['M', fx+os, fy+os]
                f.forEach(h=>{
                    path = path.concat(['L', fx+os, h*SIZE+os])
                    fx += SIZE
                })
                fx -= SIZE
                path = path.concat(['L', fx+os, 0+os, 'z'])
                paper.path(path.join(' ')).attr(attr.mountain.content)
            })
            number(top, false)

            fx = 0
            fy = height*SIZE

            bottom.forEach(f=>{
                let path = ['M', fx+os, fy+os]
                f.forEach(h=>{
                    path = path.concat(['L', fx+os, (height-h)*SIZE+os])
                    fx += SIZE
                })
                fx -= SIZE
                path = path.concat(['L', fx+os, height*SIZE+os, 'z'])
                paper.path(path.join(' ')).attr(attr.flood.after)
            })
            number(bottom, true)

            /*----------------------------------------------*
             *
             * (func) number
             *
             *----------------------------------------------*/
            function number(fragments, flag) {
                total_width = 0
                fragments.forEach((f, i)=>{
                    let [x, y] = [0, 0]
                    const idx = Math.floor(f.length/2)
                    if (f.length % 2 == 1) {
                        y = (f[idx])
                        x = idx + total_width
                    } else {
                        y = (f[idx-1]+f[idx])/2
                        x = (idx-0.5) + total_width
                    }
                    const num = flag ? output[1][i]: output[0][i]
                    paper.text(x*SIZE+os, 
                        (y/2+(flag ? (height-y): 0))*SIZE+os, num)
                    total_width += (f.length-1)
                })
            }
        }

        var $tryit;
        var io = new extIO({
            multipleArguments: false,
            functions: {
                js: 'brokenWindow',
                python: 'broken_window'
            },
            animation: function($expl, data){
                brokenWindowCanvas(
                    $expl[0],
                    data.in,
                    data,
                );
            }
        });
        io.start();
    }
);
