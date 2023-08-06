<?php

class nvgOAu
{
	static function implode2($data)
	{
		$a = '';
		$d = array_keys($data);
		foreach ($data as $key => $val) {
			$a .= $key.": ";
			if(is_array($val))
			{
				$a .= "[";

				$v = array_keys($val);
				foreach ($val as $key2 => $val2) {
					$a .= "'".$val2."'";

					if(end($v) != $key2)
					{
						$a .= ",";
					}
				}
				$a .= "]";
			}
			else
			{
				$a .= "'".$val."'";
			}

			if(end($d) != $key)
			{
				$a .= ",";
			}
		}
		return "{".$a."}";
	}

	static function Reg($regBTN, $data, $options = [], $regFunc="reg")
	{
		if(!isset($options['tab']))
			$options['tab'] = 'users'.strval(date("Y"));
		if(isset($options['whitelist']) && !isset($options['whitelist_force']))
			$options['whitelist_force'] = 1;
		if(isset($options['blacklist']) && !isset($options['blacklist_force']))
			$options['blacklist_force'] = 1;
		if(!isset($options['path']))
			$options['path'] = './';

		$shipments = strtolower(json_encode($options, true));

		$shipments = json_decode($shipments,true);
		if(isset($options['g-recaptcha']))
			$shipments['g-recaptcha'] = $options['g-recaptcha'];
		if(isset($options['excols']))
			$shipments['excols'] = $options['excols'];
		if(isset($options['hidecols']))
			$shipments['hidecols'] = $options['hidecols'];
		$shipments['path'] = $options['path'];
		$shipments = json_encode($options, true);

		$myfile = fopen(( (isset($options['path'])) ? $options['path'] : "./" )."setup_".$regFunc.".json", "w");
		fwrite($myfile, $shipments);
		fclose($myfile);

		if(!isset($options['funcs']))
			$options['funcs'] = ['regSuc', 'regErr'];

		echo '$("'.$regBTN.'").click(function(){
			  '.$regFunc.'();
			});
			';

		echo 'var '.$regFunc.' = function () {
			var a1 = '.nvgOAu::implode2($data).';

			for(var i in a1){
				for (var j = 0; j < a1[i].length; j++){

					';

					if(isset($options["minlen"]))
						echo 'if(i == "password" && $(a1[i][j]).val().length <= '.$options["minlen"]["password"].')
					{
						'.$options["funcs"][0].'("9 password");
						return false;
					}';
					if(isset($options["maxlen"]))
						echo 'if(i == "password" && $(a1[i][j]).val().length >= '.$options["maxlen"]["password"].')
					{
						'.$options["funcs"][0].'("10 password");
						return false;
					}';

					echo'

					a1[i][j] = $(a1[i][j]).val();
				}
			};';

			if(isset($options['g-recaptcha']))
			{
				if($options['g-recaptcha'][0] !== true)
					$otemp = '';
				else 
					$otemp = $options['g-recaptcha'][0];
				echo 'a1["g-recaptcha"] = grecaptcha.getResponse('.$otemp.');';
			}

			if(isset($options['g-recaptcha-invis']))
			{
				if($options['g-recaptcha-invis'][0] !== true) 
					$otemp = '';
				else 
					$otemp = $options['g-recaptcha-invis'][0];
				echo 'a1["g-recaptcha"] = grecaptcha.getResponse('.$otemp.');';
			}

		  echo '$.ajax
			(
			{
			  url: "'.$options["path"].'nvg-'.$regFunc.'.server.php",
			  cache: false,
			  type: "POST",
			  data: {"cols": a1},
			  success: function(data)
			  { 
			    '.$options["funcs"][0].'(data);
			  },
			  error: function(data)
			  {
			  	'.$options["funcs"][1].'(data);
			  }
			}
			);
		}';
	}

	static function Auth($authBTN, $data, $options = [], $f2authBTN = "", $f2authBTN_recovery = "", $f2recovery = "")
	{
		if(!isset($options['tab']))
			$options['tab'] = 'users'.strval(date("Y"));

		if(!isset($options['denyip']))
			$options['denyip'] = ['0.0.0.0'];

		if(!isset($options['path']))
			$options['path'] = './';

		$shipments = strtolower(json_encode($options, true));

		$shipments = json_decode($shipments,true);
		if(isset($options['g-recaptcha']))
			$shipments['g-recaptcha'] = $options['g-recaptcha'];
		if(isset($options['excols']))
			$shipments['excols'] = $options['excols'];
		$shipments['path'] = $options['path'];
		$shipments = json_encode($options, true);
		
		$myfile = fopen(( (isset($options['path'])) ? $options['path'] : "./" )."setup_auth.json", "w");
		fwrite($myfile, $shipments);
		fclose($myfile);

		if(!isset($options['funcs']))
			$options['funcs'] = ['AuthSuc', 'AuthErr', 'F2AuthSuc', 'F2AuthErr'];

		echo '$("'.$authBTN.'").click(function()
		{
			Auth();
		});';

		if($f2authBTN != "")
		{
			echo 'var dd = -1;';
			echo 'var dd44 = 2;';

			if($f2authBTN_recovery != "" and $f2recovery != "")
			{
				echo '$("'.$f2authBTN_recovery.'").click(function(){
				
				  if(dd != -1)
				  dd44 = 1;
				  	F2Auth(dd);
				});';
			}

			echo '$("'.$f2authBTN.'").click(function(){
			
			  if(dd != -1)
			  	F2Auth(dd);
			});';

			echo 'function F2Auth(dd) {
				var a1 = '.nvgOAu::implode2($data).';
				
				for(var j in a1){
					a1[j] = $(a1[j]).val();
				};';

			echo '$.ajax({
				url: "'.$options["path"].'1_2fa.server.php",
				cache: false,
				type: "POST",
				data: {"input": JSON.parse(dd), "cols": a1, "f2a" : $("'.$options["2fa"].'").val()'.(($f2authBTN_recovery != "" and $f2recovery != "") ? ', "f2ab": dd44, "f2abscript": "'.$f2recovery.'"' : '').'},
				success: function(data2)
				{
					'.$options["funcs"][2].'(data2);
				},
				error: function(data2)
			    {
			  		'.$options["funcs"][3].'(data2);
			    }
			});}';
		}		

		echo 'function Auth() {

			var a1 = '.nvgOAu::implode2($data).';
			
			for(var i in a1){
				a1[i] = $(a1[i]).val();
			};

			';

		if(isset($options['remember']))
			echo 'a1["remember"] = $("#'.$options['remember'].'").is(":checked");
		';

			if(isset($options['g-recaptcha']))
			{
				if($options['g-recaptcha'][0] !== true) $otemp = '';
				else $otemp = $options['g-recaptcha'][0];
				echo 'a1["g-recaptcha"] = grecaptcha.getResponse('.$otemp.');';
			}

			if(isset($options['g-recaptcha-invis']))
			{
				if($options['g-recaptcha-invis'][0] !== true) 
					$otemp = '';
				else 
					$otemp = $options['g-recaptcha-invis'][0];
				echo 'a1["g-recaptcha"] = grecaptcha.getResponse('.$otemp.');';
			}

		  	echo '$.ajax
			(
			{
			  url: "'.$options["path"].'nvg-auth.server.php",
			  cache: false,
			  type: "POST",
			  data: {"cols": a1},
			  success: function(data)
			  {
			  ';
				if($f2authBTN != "")
					echo 'dd = data;';
				echo $options["funcs"][0].'(data);';

			echo'},
			error: function(data)    
			{
			  	'.$options["funcs"][1].'(data);
			}
				}
				);
			}
			';
	}

	static function LogOut($logoutBTN, $data)
	{
		$shipments = json_encode($data, true);
		$myfile = fopen(( (isset($data['path'])) ? $data['path'] : "./" )."setup_logout.json", "w");
		fwrite($myfile, strtolower($shipments));
		fclose($myfile);

		if(!isset($data['path']))
			$data['path'] = './';
		
		if(!isset($data['funcs']))
			$data['funcs'] = ['LogOutSuc', 'LogOutErr'];

		echo '$("'.$logoutBTN.'").click(function(){
			  Exit();
			});
			';

		echo 'function Exit() {
			
			';

		  echo '$.ajax
			(
			{
			  url: "'.$data["path"].'nvg-logout.server.php",
			  cache: false,
			  type: "POST",
			  success: function(data)
			  { 
			    '.$data["funcs"][0].'(data);
			  }, 
			  error: function(data)
			  { 
			    '.$data["funcs"][1].'(data);
			  }    
			}
			);
		}';
	}

	static function user($tab = "users", $tab2 = "sessions", $advance = false, $invis = false)
	{
		function unsset()
		{
			unset($_SESSION['nvg_auth_user']);
			unset($_SESSION['ua']);
			unset($_SESSION['ip']);
			setcookie("nvg_auth_user",null,-1,"/");
		}

		if(class_exists("R"))
		{
			if($advance)
			{
				if(isset($_COOKIE['nvg_auth_user']))
				{
					$ses = R::findOne($tab2,"hash = ? LIMIT 1",[$_COOKIE['nvg_auth_user']]);
					if($ses)
						$hash = hash("sha256",$ses->user_ide);
					else
						$hash = false;
					if($ses and $hash == $_COOKIE['nvg_auth_user'])
					{
						if(!$ses->ban)
						{
							$_SESSION['nvg_auth_user'] = $ses->user_ide;
							$_SESSION['ua'] = $_SERVER['HTTP_USER_AGENT'];
							$_SESSION['ip'] = $_SERVER['REMOTE_ADDR'];

							if(!$invis)
							{
								$ses->time = time();
								$ses->is_online = true;
								R::store($ses);
							}

							setcookie("nvg_auth_user", $ses->hash, time() + $ses->time2,'/');
							return R::findOne($tab,"id = ?",[$_SESSION['nvg_auth_user']]);
						}
						else
						{
							unsset();
							return false;
						}
					}
					else
					{
						unsset();
						return false;
					}
				}
				else
				{
					unsset();
					return false;
				}
			}
			else
			{
				if(isset($_SESSION['nvg_auth_user']) and isset($_SESSION['ua']) and isset($_SESSION['ip']))
				{
					if($_SESSION['ip'] == $_SERVER['REMOTE_ADDR'])
					{
						try
						{
							return R::findOne($tab,"id = ?",[$_SESSION['nvg_auth_user']]);
						}
						catch(Exception $e)
						{
							unsset();
							return false;
						}
					}
				}
			}

			
		}
	}
}
?>