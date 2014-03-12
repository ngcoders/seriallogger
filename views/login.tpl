% include('header.tpl')
<div class="container">
	<div class="header">
        % include('menu.tpl')
        <h3 class="text-muted">Raspi Logger Downloader</h3>
      	</div>

		<div class="row">
			<div class="span12">
				<form class="form-horizontal" action='' method="POST">
				  <fieldset>
				    <div id="legend" >
				      <legend class="">Login</legend>
				    </div>
				    <div class="control-group">
				      <!-- Username -->
				      <label class="control-label"  for="username">Username</label>
				      <div class="controls">
					<input type="text" id="username" name="username" placeholder="" class="input-xlarge">
				      </div>
				    </div>
				    <div class="control-group">
				      <!-- Password-->
				      <label class="control-label" for="password">Password</label>
				      <div class="controls">
					<input type="password" id="password" name="password" placeholder="" class="input-xlarge">
				      </div>
				    </div>
				    <div class="control-group">
				      <!-- Button -->
				      <br />
				      <div class="controls">
					<button class="btn btn-success">Login</button>
				      </div>
				    </div>
				  </fieldset>
				</form>
				<hr>
			</div>
		</div>	

</div>
% include('footer.tpl')
