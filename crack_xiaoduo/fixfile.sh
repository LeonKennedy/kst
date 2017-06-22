#!/bin/sh

function top_bar()
{
    filename='lib/top_bar.pyo_dis'
    initparams='       self.kst_receiv_msgs = deque()\n        self.kst_send_msgs = deque()\n        self.kst_socket_port=62131\n        thread.start_new_thread(self.kst_socket_server, ())'  
    sed -i "/def __init__/a\ $initparams" $filename
    param1='                       self.kst_receiv_msgs.append(str(msg_list))'
    lines=$(sed -n "190,260{/self.side_windows\[snick\].add_to_chat_record_info/=}" $filename)
    for iline in $lines
    do
        sed -i "${iline}a\ $param1" $filename
    done
    sed -i '23i import select, socket' $filename
    sed -i 's/self.show()/self.hide()/g' $filename
    sed -i 's/tray.show()/#tray.show()/' $filename
    echo "" >> $filename
    cat top_bar_socket >> $filename
    echo 'fixed top_bar'
}
