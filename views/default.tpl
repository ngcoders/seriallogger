% include('header.tpl')
<div class="container">
      <div class="header">
        % include('menu.tpl')
        <h3 class="text-muted">Raspi Logger Downloader</h3>
      </div>

    <div class="panel panel-default">
  <div class="panel-heading">
    <h3 class="panel-title">Device Info </h3>
  </div>
  <div class="panel-body">

      <div class="systemstats container-fluid">
      <div class="row">
          
          <div class="col-md-4">
              <table class="table">
                <thead>
                <tr><th>System</th></tr>
                </thead>
                <tbody>
                <tr>
                  <td>Uptime</td>                  
                  <td>
                   <span>{{upTime}} </span>   
                  </td>                  
                </tr>
                <tr>
                  <td>Time</td>
                  <td>
                   <span>{{nowTime}} </span>  
                  </td>                  
                </tr>
                <tr>
                  <td>Kernel</td>
                  <td>
                   <span>{{kerVer}}</span>   
                  </td>                  
                </tr>

              </tbody>
              </table>
          </div>        

          <div class="col-md-4">
              <table class="table">
                 <thead>                  
                  <tr><th colspan=2>Network ( eth0 )</th></tr>
                </thead>
                <tbody>
                  <tr>
                  <td>Hostname</td>
                    <td>
                      <span>{{hostNameIs}}</span>                         
                  </td></tr>
                  <tr>
                    <td>IP</td>
                    <td>
                      <span>{{ipAddrEth0}}</span>                        
                  </td></tr>
                  <tr>
                    <td>Netmask</td>
                    <td>
                      <span>{{netMaskField}}</span>                                          
                </tbody>
              </table>
          </div>        

          <div class="col-md-4">
              <table class="table">
                  <thead>    
                  <tr><th>Disk ( / ) </th></tr>
                  </thead>
                  <tbody>
                  <tr>
                      <td>Total</td>
                      <td>
                      <span>{{totalNetSpace}}</span>                        
                  </td></tr>
                  <tr>
                    <td>Free</td>
                    <td>
                      <span>{{notUsed}}</span>                         
                  </td></tr>
                  <tr>
                    <td>Used</td>  
                    <td>
                      <span>{{usedSpace}}</span                  
                </tbody>

              </table>
          </div>        

      </div>
      </div>

</div>
</div>

      <div class="panel panel-default">
  <div class="panel-heading">
    <h3 class="panel-title">Log Files</h3>
  </div>
  <div class="panel-body">



      <div class="files">
        % import os,functions
        <table class="table table-striped"> 
          <thead>
          <tr>
            <th style="width:50%">Device Logs</th>
            <th style="width:10%">Size</th>
            <th style="text-align:center;">Options</th>          
          </tr>
          </thead>
          <tbody>
          % for file in files: 
            <tr>
                <td>{{file}}</td>
                <td>                
                % size = functions.sizeof_fmt ( os.path.getsize('logs/'+file) )
                {{size}}
                </td>
                <td style="text-align:center;">
                  <a href="download/{{file}}" class="btn btn-primary btn-xs">Download</a>
                  <a onclick="return confirm('Are you sure you wish to truncate {{file}} ?');" href="truncate/{{file}}" class="btn btn-primary btn-xs">Truncate</a>
                  <a onclick="return confirm('Are you sure you wish to delete {{file}} ?');" href="delete/{{file}}" class="btn btn-primary btn-xs">Delete</a>
                </td>
            </tr>
          % end
          </tbody>
        </table>

      </div>

</div>

</div>

</div>      
% include('footer.tpl')

