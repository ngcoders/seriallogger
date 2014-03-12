% include('header.tpl')
<div class="container">
      <div class="header">
        % include('menu.tpl')
        <h3 class="text-muted">Raspi Logger Downloader</h3>
      </div>

      <form role="form" class="form-horizontal" method="POST">
  
	%for section in config.sections():
	%	section_name = section
	%	device = config.get(section,'device')
	%	baudrate = config.get(section,'baudrate')
	%	gpio = config.get(section,'gpio')

	  <div class="panel panel-default">
  		<div class="panel-heading">
    	<h3 class="panel-title">
    		{{section_name}}
    	</h3>
  		</div>
  		<div class="panel-body">

	      	<div class="row">
			<div class="col-xs-4">
			    <label>Device</label>
			    <input type="text" class="form-control" name="{{section_name}}" value = "{{device}}" required> 
			</div>
			<div class="col-xs-3">
			    <label>Baudrate</label>
			    <input type="number" class="form-control" name="{{section_name}}"  value = "{{baudrate}}" required> 
			</div>		


			<div class="col-xs-3">
			    <label>GPIO</label>
			    <input type="number" class="col-lg-6 form-control" name="{{section_name}}" value="{{gpio}}"  data-bind="value:replyNumber" required> 
			</div>
			</div>

		</div>
		</div>
	%end

<button type="submit" class="btn btn-primary">Save Settings</button>
</form>

<hr>
		<a href="/reboot">
		<button type="button" class="btn btn-primary">Reboot Logger</button>
		</a>
<br>
<hr>
</div>

% include('footer.tpl')

