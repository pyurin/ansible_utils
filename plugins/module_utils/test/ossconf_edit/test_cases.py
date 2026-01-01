test_cases = [
    {   # basic value change test
        "xml_from": """
            <ossec_config>
              <client>
                <server>
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>
            </ossec_config>
        """,
        "xpath": "/ossec_config/client/server/address",
        "value": "10.0.0.1",
        "xml_to": """
            <ossec_config>
              <client>
                <server>
                  <address>10.0.0.1</address>
                </server>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>
            </ossec_config>
        """,
    },
    {   # negative test, same as previous but to check that node lists are preserved
        "should_match": False,
        "xml_from": """
            <ossec_config>
              <client>
                <server>
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>
            </ossec_config>
        """,
        "xpath": "/ossec_config/client/server/address",
        "value": "10.0.0.1",
        "xml_to": """
            <ossec_config>
              <client>
                <server>
                  <address>10.0.0.1</address>
                </server>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>
            </ossec_config>
        """,
    },
    {   # value add, test 1
        "xml_from": """
            <ossec_config>
              <client>
                <server>
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>
            </ossec_config>
        """,
        "xpath": "/ossec_config/client/enrollment/agent_name",
        "value": "some_agent_name",
        "xml_to": """
            <ossec_config>
              <client>
                <server>
                  <address>addr</address>
                </server>
                <enrollment>
                    <agent_name>some_agent_name</agent_name>
                </enrollment>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>
            </ossec_config>
        """,
    },
    {   # value add, test 2
        "xml_from": """
            <ossec_config>
              <client>
                <server>
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>
            </ossec_config>
        """,
        "xpath": "/ossec_config/localfile/temp_param",
        "value": "some_agent_name",
        "xml_to": """
            <ossec_config>
              <client>
                <server>
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
                <temp_param>some_agent_name</temp_param>
              </localfile>
            </ossec_config>
        """,
    },
    {   # list edit
        "xml_from": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
              </localfile>            
            </ossec_config>
        """,
        "xpath": "/ossec_config/localfile[location='journald']/log_format",
        "value": "journald+modified",
        "xml_to": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald+modified</log_format>
                <location>journald</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
              </localfile>            
            </ossec_config>
        """,
    },
    {   # list edit 2
        "xml_from": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
              </localfile>            
            </ossec_config>
        """,
        "xpath": "/ossec_config/localfile[location='journald']/frequency",
        "value": "56",
        "xml_to": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
                <frequency>56</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
              </localfile>            
            </ossec_config>
        """,
    },
    {   # list edit 3
        "xml_from": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
                <frequency>30</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
              </localfile>            
            </ossec_config>
        """,
        "xpath": "/ossec_config/localfile/frequency",
        "value": "61",
        "xml_to": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
                <frequency>61</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
                <frequency>61</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
                <frequency>61</frequency>
              </localfile>            
            </ossec_config>
        """,
    },
    {   # list edit 4
        "xml_from": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
                <frequency>30</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
              </localfile>            
            </ossec_config>
        """,
        "xpath": "/ossec_config/localfile[log_format='apache']/frequency",
        "value": "61",
        "xml_to": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
                <frequency>30</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
                <frequency>61</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
                <frequency>61</frequency>
              </localfile>            
            </ossec_config>
        """,
    },
    {   # list edit 5
        "xml_from": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
                <frequency>30</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
              </localfile>            
            </ossec_config>
        """,
        "xpath": "/ossec_config/localfile[location='/var/log/nginx/access.log']/frequency",
        "value": "61",
        "xml_to": """
            <ossec_config>
              <client>
              </client>
            </ossec_config>
            <ossec_config>
              <localfile>
                <log_format>journald</log_format>
                <location>journald</location>
                <frequency>30</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/access.log</location>
                <frequency>61</frequency>
              </localfile>            
              <localfile>
                <log_format>apache</log_format>
                <location>/var/log/nginx/error.log</location>
              </localfile>            
            </ossec_config>
        """,
    },
    {   # list edit 6
        "xml_from": """
                <!--
                  Wazuh - Agent - Default configuration for darwin 25.2
                  More info at: https://documentation.wazuh.com
                  Mailing list: https://groups.google.com/forum/#!forum/wazuh
                -->
                
                <ossec_config>
                  <client>
                    <server>
                      <address>localhost</address>
                      <port>1514</port>
                      <protocol>tcp</protocol>
                    </server>
                    <config-profile>darwin, darwin25, darwin25.2</config-profile>
                    <notify_time>20</notify_time>
                    <time-reconnect>60</time-reconnect>
                    <auto_restart>yes</auto_restart>
                    <crypto_method>aes</crypto_method>
                  </client>
                
                  <client_buffer>
                    <!-- Agent buffer options -->
                    <disabled>no</disabled>
                    <queue_size>5000</queue_size>
                    <events_per_second>500</events_per_second>
                  </client_buffer>
                
                  <!-- Policy monitoring -->
                  <rootcheck>
                    <disabled>no</disabled>
                    <check_files>yes</check_files>
                    <check_trojans>yes</check_trojans>
                    <check_dev>yes</check_dev>
                    <check_sys>yes</check_sys>
                    <check_pids>yes</check_pids>
                    <check_ports>yes</check_ports>
                    <check_if>yes</check_if>
                
                    <!-- Frequency that rootcheck is executed - every 12 hours -->
                    <frequency>43200</frequency>
                
                    <rootkit_files>etc/shared/rootkit_files.txt</rootkit_files>
                    <rootkit_trojans>etc/shared/rootkit_trojans.txt</rootkit_trojans>
                
                    <skip_nfs>yes</skip_nfs>
                
                    <ignore>/var/lib/containerd</ignore>
                    <ignore>/var/lib/docker/overlay2</ignore>
                  </rootcheck>
                
                  <!-- Osquery integration -->
                  <wodle name="osquery">
                    <disabled>yes</disabled>
                    <run_daemon>yes</run_daemon>
                    <log_path>/var/log/osquery/osqueryd.results.log</log_path>
                    <config_path>/etc/osquery/osquery.conf</config_path>
                    <add_labels>yes</add_labels>
                  </wodle>
                
                  <!-- System inventory -->
                  <wodle name="syscollector">
                    <disabled>no</disabled>
                    <interval>1h</interval>
                    <scan_on_start>yes</scan_on_start>
                    <hardware>yes</hardware>
                    <os>yes</os>
                    <network>yes</network>
                    <packages>yes</packages>
                    <ports all="yes">yes</ports>
                    <processes>yes</processes>
                    <users>yes</users>
                    <groups>yes</groups>
                    <services>yes</services>
                    <browser_extensions>yes</browser_extensions>
                
                    <!-- Database synchronization settings -->
                    <synchronization>
                      <max_eps>10</max_eps>
                    </synchronization>
                  </wodle>
                
                  <sca>
                    <enabled>yes</enabled>
                    <scan_on_start>yes</scan_on_start>
                    <interval>12h</interval>
                    <skip_nfs>yes</skip_nfs>
                  </sca>
                  
                  <!-- File integrity monitoring -->
                  <syscheck>
                    <disabled>no</disabled>
                
                    <!-- Frequency that syscheck is executed default every 12 hours -->
                    <frequency>43200</frequency>
                
                    <scan_on_start>yes</scan_on_start>
                
                    <!-- Directories to check  (perform all possible verifications) -->
                    <directories>/etc,/usr/bin,/usr/sbin</directories>
                    <directories>/bin,/sbin</directories>
                
                    <!-- Files/directories to ignore -->
                    <ignore>/etc/mtab</ignore>
                    <ignore>/etc/hosts.deny</ignore>
                    <ignore>/etc/mail/statistics</ignore>
                    <ignore>/etc/random-seed</ignore>
                    <ignore>/etc/random.seed</ignore>
                    <ignore>/etc/adjtime</ignore>
                    <ignore>/etc/httpd/logs</ignore>
                    <ignore>/etc/utmpx</ignore>
                    <ignore>/etc/wtmpx</ignore>
                    <ignore>/etc/cups/certs</ignore>
                    <ignore>/etc/dumpdates</ignore>
                    <ignore>/etc/svc/volatile</ignore>
                
                    <!-- File types to ignore -->
                    <ignore type="sregex">.log$|.swp$</ignore>
                
                    <!-- Check the file, but never compute the diff -->
                    <nodiff>/etc/ssl/private.key</nodiff>
                
                    <skip_nfs>yes</skip_nfs>
                    <skip_dev>yes</skip_dev>
                    <skip_proc>yes</skip_proc>
                    <skip_sys>yes</skip_sys>
                
                    <!-- Nice value for Syscheck process -->
                    <process_priority>10</process_priority>
                
                    <!-- Maximum output throughput -->
                    <max_eps>50</max_eps>
                
                    <!-- Database synchronization settings -->
                    <synchronization>
                      <enabled>yes</enabled>
                      <interval>5m</interval>
                      <max_eps>10</max_eps>
                    </synchronization>
                  </syscheck>
                
                  <!-- Log analysis -->
                  <localfile>
                    <log_format>full_command</log_format>
                    <command>netstat -an | awk '{if ((/^(tcp|udp)/) && ($4 != "*.*") && ($5 == "*.*")) {print $1" "$4" "$5}}' | sort -u</command>
                    <alias>netstat listening ports</alias>
                    <frequency>360</frequency>
                  </localfile>
                
                  <localfile>
                    <location>macos</location>
                    <log_format>macos</log_format>
                    <query type="trace,log,activity" level="info">(process == "sudo") or (process == "sessionlogoutd" and message contains "logout is complete.") or (process == "sshd") or (process == "tccd" and message contains "Update Access Record") or (message contains "SessionAgentNotificationCenter") or (process == "screensharingd" and message contains "Authentication") or (process == "securityd" and eventMessage contains "Session" and subsystem == "com.apple.securityd")</query>
                  </localfile>
                
                  <!-- Active response -->
                  <active-response>
                    <disabled>no</disabled>
                    <ca_store>etc/wpk_root.pem</ca_store>
                    <ca_verification>yes</ca_verification>
                  </active-response>
                
                  <!-- Choose between "plain", "json", or "plain,json" for the format of internal logs -->
                  <logging>
                    <log_format>plain</log_format>
                  </logging>
                
                </ossec_config>
        """,
        "xpath": "/ossec_config/localfile[location='macos']/frequency",
        "value": "61",
        "xml_to": """
                <!--
                  Wazuh - Agent - Default configuration for darwin 25.2
                  More info at: https://documentation.wazuh.com
                  Mailing list: https://groups.google.com/forum/#!forum/wazuh
                -->
                
                <ossec_config>
                  <client>
                    <server>
                      <address>localhost</address>
                      <port>1514</port>
                      <protocol>tcp</protocol>
                    </server>
                    <config-profile>darwin, darwin25, darwin25.2</config-profile>
                    <notify_time>20</notify_time>
                    <time-reconnect>60</time-reconnect>
                    <auto_restart>yes</auto_restart>
                    <crypto_method>aes</crypto_method>
                  </client>
                
                  <client_buffer>
                    <!-- Agent buffer options -->
                    <disabled>no</disabled>
                    <queue_size>5000</queue_size>
                    <events_per_second>500</events_per_second>
                  </client_buffer>
                
                  <!-- Policy monitoring -->
                  <rootcheck>
                    <disabled>no</disabled>
                    <check_files>yes</check_files>
                    <check_trojans>yes</check_trojans>
                    <check_dev>yes</check_dev>
                    <check_sys>yes</check_sys>
                    <check_pids>yes</check_pids>
                    <check_ports>yes</check_ports>
                    <check_if>yes</check_if>
                
                    <!-- Frequency that rootcheck is executed - every 12 hours -->
                    <frequency>43200</frequency>
                
                    <rootkit_files>etc/shared/rootkit_files.txt</rootkit_files>
                    <rootkit_trojans>etc/shared/rootkit_trojans.txt</rootkit_trojans>
                
                    <skip_nfs>yes</skip_nfs>
                
                    <ignore>/var/lib/containerd</ignore>
                    <ignore>/var/lib/docker/overlay2</ignore>
                  </rootcheck>
                
                  <!-- Osquery integration -->
                  <wodle name="osquery">
                    <disabled>yes</disabled>
                    <run_daemon>yes</run_daemon>
                    <log_path>/var/log/osquery/osqueryd.results.log</log_path>
                    <config_path>/etc/osquery/osquery.conf</config_path>
                    <add_labels>yes</add_labels>
                  </wodle>
                
                  <!-- System inventory -->
                  <wodle name="syscollector">
                    <disabled>no</disabled>
                    <interval>1h</interval>
                    <scan_on_start>yes</scan_on_start>
                    <hardware>yes</hardware>
                    <os>yes</os>
                    <network>yes</network>
                    <packages>yes</packages>
                    <ports all="yes">yes</ports>
                    <processes>yes</processes>
                    <users>yes</users>
                    <groups>yes</groups>
                    <services>yes</services>
                    <browser_extensions>yes</browser_extensions>
                
                    <!-- Database synchronization settings -->
                    <synchronization>
                      <max_eps>10</max_eps>
                    </synchronization>
                  </wodle>
                
                  <sca>
                    <enabled>yes</enabled>
                    <scan_on_start>yes</scan_on_start>
                    <interval>12h</interval>
                    <skip_nfs>yes</skip_nfs>
                  </sca>
                  
                  <!-- File integrity monitoring -->
                  <syscheck>
                    <disabled>no</disabled>
                
                    <!-- Frequency that syscheck is executed default every 12 hours -->
                    <frequency>43200</frequency>
                
                    <scan_on_start>yes</scan_on_start>
                
                    <!-- Directories to check  (perform all possible verifications) -->
                    <directories>/etc,/usr/bin,/usr/sbin</directories>
                    <directories>/bin,/sbin</directories>
                
                    <!-- Files/directories to ignore -->
                    <ignore>/etc/mtab</ignore>
                    <ignore>/etc/hosts.deny</ignore>
                    <ignore>/etc/mail/statistics</ignore>
                    <ignore>/etc/random-seed</ignore>
                    <ignore>/etc/random.seed</ignore>
                    <ignore>/etc/adjtime</ignore>
                    <ignore>/etc/httpd/logs</ignore>
                    <ignore>/etc/utmpx</ignore>
                    <ignore>/etc/wtmpx</ignore>
                    <ignore>/etc/cups/certs</ignore>
                    <ignore>/etc/dumpdates</ignore>
                    <ignore>/etc/svc/volatile</ignore>
                
                    <!-- File types to ignore -->
                    <ignore type="sregex">.log$|.swp$</ignore>
                
                    <!-- Check the file, but never compute the diff -->
                    <nodiff>/etc/ssl/private.key</nodiff>
                
                    <skip_nfs>yes</skip_nfs>
                    <skip_dev>yes</skip_dev>
                    <skip_proc>yes</skip_proc>
                    <skip_sys>yes</skip_sys>
                
                    <!-- Nice value for Syscheck process -->
                    <process_priority>10</process_priority>
                
                    <!-- Maximum output throughput -->
                    <max_eps>50</max_eps>
                
                    <!-- Database synchronization settings -->
                    <synchronization>
                      <enabled>yes</enabled>
                      <interval>5m</interval>
                      <max_eps>10</max_eps>
                    </synchronization>
                  </syscheck>
                
                  <!-- Log analysis -->
                  <localfile>
                    <log_format>full_command</log_format>
                    <command>netstat -an | awk '{if ((/^(tcp|udp)/) && ($4 != "*.*") && ($5 == "*.*")) {print $1" "$4" "$5}}' | sort -u</command>
                    <alias>netstat listening ports</alias>
                    <frequency>360</frequency>
                  </localfile>
                
                  <localfile>
                    <location>macos</location>
                    <log_format>macos</log_format>
                    <query type="trace,log,activity" level="info">(process == "sudo") or (process == "sessionlogoutd" and message contains "logout is complete.") or (process == "sshd") or (process == "tccd" and message contains "Update Access Record") or (message contains "SessionAgentNotificationCenter") or (process == "screensharingd" and message contains "Authentication") or (process == "securityd" and eventMessage contains "Session" and subsystem == "com.apple.securityd")</query>
                    <frequency>61</frequency>
                  </localfile>
                
                  <!-- Active response -->
                  <active-response>
                    <disabled>no</disabled>
                    <ca_store>etc/wpk_root.pem</ca_store>
                    <ca_verification>yes</ca_verification>
                  </active-response>
                
                  <!-- Choose between "plain", "json", or "plain,json" for the format of internal logs -->
                  <logging>
                    <log_format>plain</log_format>
                  </logging>
                
                </ossec_config>
        """,
    },
    {   # list edit 7
        "xml_from": """
                <ossec_config>                
                </ossec_config>
                <ossec_config>                
                </ossec_config>
        """,
        "xpath": "/ossec_config[1]/integration[name='test_name']/name",
        "value": "test_name",
        "xml_to": """
                <ossec_config>       
                    <integration>
                        <name>test_name</name>
                    </integration>         
                </ossec_config>
                <ossec_config>                
                </ossec_config>
        """,
    },
    {
        "xml_from": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>          
            """,
        "xpath": "/group[@name='syslog,sshd,']",
        "attributes": {
            "name": "syslog,sshd,"
        },
        "xml_to": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
                <group name="syslog,sshd,">
                </group>
            """,
    },
    {
        "xml_from": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
                <group name="syslog,sshd,">
                </group>   
            """,
        "xpath": "/group[@name='syslog,sshd,']/rule[@id='99904']",
        "attributes": {
            "id": "99904",
            "level": "9",
            "overwrite": "yes",
        },
        "xml_to": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
                <group name="syslog,sshd,">
                    <rule id="99904" level="9" overwrite="yes">
                    </rule>
                </group>
            """,
    },
    {
        "xml_from": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
            """,
        "task_block": [
            {
                "xpath": "/group[@name='syslog,sshd,']",
                "attributes": {
                    "name": "syslog,sshd,",
                    "text_att": "test_val"
                }
            },
            {
                "xpath": "/group[@name='syslog,sshd,']/rule[@id='99904']",
                "attributes": {
                    "id": "99904",
                    "level": "9",
                    "overwrite": "yes",
                },
            },
            {
                "xpath": "/group[@name='syslog,sshd,']/rule[@id='99904']/if_sid",
                "value": "9932323"
            },
        ],
        "xml_to": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
                <group name="syslog,sshd," text_att="test_val">
                    <rule id="99904" level="9" overwrite="yes">
                        <if_sid>9932323</if_sid>
                    </rule>
                </group>
            """,
    },
    {
        "xml_from": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
            """,
        "xpath": "/group[@name='webapp,']",
        "xml_set_raw": {
             """
                <group name="webapp,">
                    <rule id="100300" level="7">
                        <match>[WebApp log]</match>
                        <description>WeApp log</description>
                    </rule>
                    <rule id="100301" level="7">
                        <if_sid>100300</if_sid>
                        <match>authentication_succeeded</match>
                        <description>WeApp log, auth succeeded</description>
                        <group>authentication_succeeded,</group>
                    </rule>
                </group>
             """
        },
        "xml_to": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
                <group name="webapp,">
                    <rule id="100300" level="7">
                        <match>[WebApp log]</match>
                        <description>WeApp log</description>
                    </rule>
                    <rule id="100301" level="7">
                        <if_sid>100300</if_sid>
                        <match>authentication_succeeded</match>
                        <description>WeApp log, auth succeeded</description>
                        <group>authentication_succeeded,</group>
                    </rule>
                </group>
            """,
    },
    {
        "xml_from": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
                <group name="webapp,">
                    <rule id="100300" level="7">
                        <match>something</match>
                    </rule>
                </group>
            """,
        "xpath": "/group[@name='webapp,']",
        "xml_set_raw": {
            """
               <group name="webapp,">
                   <rule id="100300" level="7">
                       <match>[WebApp log]</match>
                       <description>WeApp log</description>
                   </rule>
                   <rule id="100301" level="7">
                       <if_sid>100300</if_sid>
                       <match>authentication_succeeded</match>
                       <description>WeApp log, auth succeeded</description>
                       <group>authentication_succeeded,</group>
                   </rule>
               </group>
            """
        },
        "xml_to": """
                <group name="some_group,">
                    <rule id="001" level="9" overwrite="yes">
                    </rule>
                </group>
                <group name="webapp,">
                    <rule id="100300" level="7">
                        <match>[WebApp log]</match>
                        <description>WeApp log</description>
                    </rule>
                    <rule id="100301" level="7">
                        <if_sid>100300</if_sid>
                        <match>authentication_succeeded</match>
                        <description>WeApp log, auth succeeded</description>
                        <group>authentication_succeeded,</group>
                    </rule>
                </group>
            """,
    },
    {
        "xml_from": """
            <ossec_config>
              <client>
                <server>
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
        """,
        "xpath": "/ossec_config/client/server/address",
        "value": "10.0.0.1",
        "when_xpath_exist": "/ossec_config/client/server/address",
        "xml_to": """
            <ossec_config>
              <client>
                <server>
                  <address>10.0.0.1</address>
                </server>
              </client>
            </ossec_config>
        """,
    },
    {
        "xml_from": """
            <ossec_config>
              <client>
                <server_other>
                  <address>addr</address>
                </server_other>
              </client>
            </ossec_config>
        """,
        "xpath": "/ossec_config/client/server/address",
        "value": "10.0.0.1",
        "when_xpath_exist": "/ossec_config/client/server/address",
        "xml_to": """
            <ossec_config>
              <client>
                <server_other>
                  <address>addr</address>
                </server_other>
              </client>
            </ossec_config>
        """,
    },
    {
        "xml_from": """
            <ossec_config>
              <client>
                <server id="1">
                  <address>addr</address>
                </server>
                <server id="2">
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
        """,
        "xpath": "/ossec_config/client/server[@id='1']/address",
        "value": "10.0.0.1",
        "when_xpath_exist": "/ossec_config/client/server[@id='1']/address",
        "xml_to": """
            <ossec_config>
              <client>
                <server id="1">
                  <address>10.0.0.1</address>
                </server>
                <server id="2">
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
        """,
    },
    {
        "xml_from": """
            <ossec_config>
              <client>
                <server id="1">
                  <address>addr</address>
                </server>
                <server id="2">
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
        """,
        "xpath": "/ossec_config/client/server[@id='3']/address",
        "value": "10.0.0.1",
        "when_xpath_exist": "/ossec_config/client/server[@id='3']/address",
        "xml_to": """
            <ossec_config>
              <client>
                <server id="1">
                  <address>addr</address>
                </server>
                <server id="2">
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
        """,
    },
    {
        "xml_from": """
            <ossec_config>
              <client>
                <server id="1">
                  <address>addr2</address>
                </server>
                <server id="2">
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
        """,
        "xpath": "/ossec_config/client/server[address='addr2']/info",
        "value": "data",
        "when_xpath_exist": "/ossec_config/client/server[address='addr2']",
        "xml_to": """
            <ossec_config>
              <client>
                <server id="1">
                  <address>addr2</address>
                  <info>data</info>
                </server>
                <server id="2">
                  <address>addr</address>
                </server>
              </client>
            </ossec_config>
        """,
    },
]

