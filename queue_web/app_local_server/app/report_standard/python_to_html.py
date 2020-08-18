def get_html(matrix, title, html_output_path):
    """ data matrix to html"""
    import os

    def get_table(table_matrix, head):
        """form html table tag"""
        # table head line
        th_txt = ''
        for i in head:
            th_txt += '<th scope="col">%s</th>\n' % i
        # table tag base
        table = """                                                 
        <table class="hor-zebra">
            <thead>
                <tr>
                    %s
                </tr>
            </thead>
            <tbody>""" % th_txt

        for i in range(len(table_matrix[0])):                       # get how many lines
            if i % 2 == 0:                                          # add color for odd line
                color_bar = 'class="odd"'
            else:
                color_bar = ''
            table += '\n<tr %s>' % color_bar                        # <tr> is line, <td> is data item
            for j in range(len(table_matrix)):                      # insert data
                table += '\n<td>' + table_matrix[j][i] + '</td>'
            table += '\n</tr>'

        table += '\n</tbody>'+'\n</table>'                          # finish table

        return table

    def get_picture_div(result_path):
        picture_list = list()
        pic_name_list = list()
        total_picture_div = str()
        for file in os.listdir(result_path):
            if file.endswith('jpg') or file.endswith('png'):
                pic_name_list.append(file.split('.')[0])
                picture_list.append(file)
        print(pic_name_list)
        print(picture_list)
        for index, pic in enumerate(picture_list):
            total_picture_div += """
            <div class="lineblock"></div>
            <h4 style="font-size:30px">%s</h4>
            <img src="%s" width = 900px  />
        """ % (pic_name_list[index], pic)

        return total_picture_div

    # create all table in html1
    volume_table = get_table(matrix[0:3], ['Volume Flow Rate', '(L/S)', 'Percentage%'])
    sp_table = get_table(matrix[3:5], ['Static Pressure', '(Pa)'])
    tp_table = get_table(matrix[5:7], ['Total Pressure', '(Pa)'])
    uni_table = get_table(matrix[7:9], ['Uniformity', ' '])
    moment_table = get_table(matrix[9:10], ['Torque(N/M)'])
    picture_div = get_picture_div(html_output_path)


    # output to HTML
    ResultHtml = html_output_path + title + ".html"
    report = open(ResultHtml, 'w')                                  # create html

    # main frame for html
    message = """
    <html>
    <head>
        <style type="text/css">
            .hor-zebra
            {
                font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                font-size: 15px;
                
                text-align: left;
                border-collapse: collapse;
            }
            .hor-zebra th
            {
                font-size: 20px;
                font-weight: normal;
                width: 200px;
                padding: 10px 8px;
                color: #039;
            }
            .hor-zebra td
            {
            
                padding: 8px;
                color: #000;
            }
            .hor-zebra .odd
            {
                background: #e8edff; 
            }
            
            
            .lineblock{
                width:90%%;
                height:1.5px;
                margin:30px;
                background:linear-gradient(to left,#efefef,#ADADAD,#efefef);
            }
        </style>
    </head>
    <body>
         <div style="text-align:center;margin-top:20px;margin-bottom:10px">
         <h2 style="font-size:54px;display:inline;">%s</h2>
         
         </div>
         <div style="margin-top:5px;padding:0;text-align:center;">
         <span>File Location: %s </span><span>&nbsp;&nbsp;&nbsp;</span>
         <span> Author: Zonghui.Jin</span>
         </div>
         
         <div class="lineblock"></div>
    
    <body style="margin-left:120px;margin-right:120px" >
        <div summary = volume flow table">%s</div>
        <div class="lineblock"></div>
        <div>%s</div>
        
        <div class="lineblock"></div>
        <div>%s</div>
        
        <div class="lineblock"></div>
        <div>%s</div>
        
        <div class="lineblock"></div>
        <div>%s</div>
        
        %s

    </body>
    </html>""" % (title, html_output_path, volume_table, sp_table, tp_table, uni_table, moment_table, picture_div)

    report.write(message)
    report.close()
    # os.system(r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s' % ResultHtml)
