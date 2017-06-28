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
    param2='       self.hide()'
    sed -i "/def detect_users/a\ $param2" $filename
    sed -i 's/self.show()/self.hide()/g' $filename
    sed -i 's/tray.show()/#tray.show()/' $filename
    echo "" >> $filename
    cat top_bar_socket >> $filename
}

function side_windows()
{
    filename='lib/side_window.pyo_dis'
    param1='       self.is_show = 0'
#hide self
    sed -i "257a\ $param1" $filename
#hide down lite window
    sed -i 's/self.half_auto_lite_window.show(/self.half_auto_lite_window.hide(/g' $filename
#hide lite-side window
    sed -i '/self.side_window_lite_window.show/d' $filename
    # crack auth
    sed -i "s/user_info.get('day_to_expire', -1)/1/" $filename
    sed -i "s/or check_msg_setting.get('asked', {}).get('enabled', False)//" side_window.pyo_dis
}

