<?php
/*Require RedBeanPHP*/
/*Work with columns: wsite, !info!, value, !lang!, !timestamp!*/

define('counter_ignore_ips', array('127.0.0.1', '127.0.0.2','console'));
define("counter_ignore_agents",array('Yandex', 'Googlebot', 'Bingbot', 'Slurp', 'DuckDuckBot', 'Baiduspider', 'YandexBot', 'facebot', 'ia_archiver', 'bot','Bot','AhrefsBot','DotBot','MJ12bot','bingbot','msnbot','SeznamBot','vkShare','facebookexternalhit','TwitterBot'));
define('blockOrgs', array("google","yandex","facebook","amazon","cloudsigma","vkontakte","mail.ru","datacamp","hetzner","microsoft","telegram","amazon.com","dataweb","digitalocean","oracle","seznam","ovh sas","reg.ru","azure"));

class nvgCount
{
	public function __construct(
		$db,
		$table,
		$resource = 'site',
		$counter_expire = 10,
		$stricter = true,
		$counter_ignore_agents = counter_ignore_agents,
		$counter_ignore_ips = counter_ignore_ips
		)
	{
		$this->db = $db;
		$this->tab = $table;
		$this->tab2 = $table;
		$this->resource = $resource;
		$this->langc = false;
		$this->stricter = $stricter;
		$this->counter_expire = $counter_expire;
		$this->counter_ignore_agents = $counter_ignore_agents;
		$this->counter_ignore_ips = $counter_ignore_ips;
	}

	public function Count()
	{
		try
		{
			R::selectDatabase($this->db);
		}
		catch(Exception $e) { die("No rb"); }

		$counter_agent = (isset($_SERVER['HTTP_USER_AGENT'])) ? $_SERVER['HTTP_USER_AGENT'] : 'bot';
		$counter_ip = (isset($_SERVER['REMOTE_ADDR'])) ? $_SERVER['REMOTE_ADDR'] : 'console'; 
		$counter_time = time();
		$ignore = false;

		for($i = 0; $i < count($this->counter_ignore_ips); $i++)
		{
			if($counter_ip == $this->counter_ignore_ips[$i])
			{
				$ignore = true;
				break;
			}
		}

		for($i = 0; $i < count($this->counter_ignore_agents); $i++)
		{
			if(substr_count(strtolower($counter_agent),strtolower($this->counter_ignore_agents[$i])))
			{
				$ignore = true;
				break;
			}
		}

		if(!$ignore)
		{
			$url = 'https://api.nvg-group.com/botIp.php?list';
			$curl = curl_init($url);
		    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		    curl_setopt($curl, CURLOPT_POST, true);
		    curl_setopt($curl, CURLOPT_TIMEOUT, 2);
		    $res = curl_exec($curl);
		    curl_close($curl);

			if(in_array($counter_ip, json_decode($res)))
				$ignore = true;
		}

		if(!$ignore and $this->stricter)
		{
			$res = shell_exec("host ".$counter_ip);

			for($i = 0; $i < count(blockOrgs); $i++)
			{
				if(substr_count(strtolower($res),strtolower(blockOrgs[$i])))
				{
					$ignore = true;
					break;
				}
			}
		}

		if(!$ignore)
		{
			$visitor = R::findOne($this->tab,'wsite = ?',[$this->resource]);

			if($visitor)
			{
				$lastIP = json_decode($visitor->info)[0];
				$lastT = json_decode($visitor->info)[1];

				if((time()-$lastT) > $this->counter_expire)
				{
					$this->doCount($counter_ip, $visitor);
				}
				else
				{
					if($lastIP != $counter_ip && (time()-$lastT) > ($this->counter_expire/2))
					{
						$this->doCount($counter_ip, $visitor);
					}
				}
			}
			else
			{
				$visitor = R::dispense($this->tab);
				$visitor->value = 0;
				$visitor->wsite = $this->resource;
				$this->doCount($counter_ip, $visitor);
			}
		}

		R::selectDatabase('default');
	}

	protected function doCount($ip, $c)
	{
		$c->value++;
		$c->info = json_encode([$ip,strval(time())]);
		R::store($c);

		if($this->langc)
			$this->countLang();
	}

	protected function countLang()
	{
		$myLang = (isset($_SERVER['HTTP_ACCEPT_LANGUAGE'])) ? $_SERVER['HTTP_ACCEPT_LANGUAGE'] : 'unknown';
		$myLang = explode(',', $myLang)[0];
		if(R::findOne($this->tab2,'lang = ? and wsite = ?',[$myLang, $this->resource]))
		{
			$con = R::findOne($this->tab2,'lang = ? and wsite = ?',[$myLang, $this->resource]);
			$con->value++;
			$con->timestamp = strval(time());
			R::store($con);
		}
		else
		{
			$con = R::dispense($this->tab2);
			$con->wsite = $this->resource;
			$con->timestamp = strval(time());
			$con->value = 1;
			$con->lang = $myLang;
			R::store($con);
		}
	}

	public function enableLangC($table)
	{
		$this->langc = true;
		$this->tab2 = $table;
	}
}

class nvgData
{
	public function __construct($db, $table, $t, $resource, $counter_expire = 7, $collectUA = false, $httpRefers = false)
	{
		$this->tab = $table;
		$this->resource = $resource;
		$this->httpRefers = $httpRefers;
		$this->collectUA = $collectUA;
		$this->counter_expire = ($counter_expire) ? $counter_expire : 7;

		try
		{
			R::selectDatabase($db);
		}
		catch(Exception $e) { die("No rb"); }

		switch ($t)
		{
			case 'ip':
				$this->collectIP();
				break;
			default:
				break;
		}

		try
		{
			R::selectDatabase('default');
		}
		catch(Exception $e) { die("ERROR"); }
	}

	public function collectIP()
	{
		$myip = (isset($_SERVER['REMOTE_ADDR'])) ? $_SERVER['REMOTE_ADDR'] : 'console';
		$counter_agent = (isset($_SERVER['HTTP_USER_AGENT'])) ? $_SERVER['HTTP_USER_AGENT'] : 'bot';
		$ignore = false;

		for($i = 0; $i < count(counter_ignore_agents); $i++)
		{
			if(substr_count(strtolower($counter_agent),strtolower(counter_ignore_agents[$i])))
			{
				$ignore = true;
				break;
			}
		}

		$res = shell_exec("host ".$myip);

		for($i = 0; $i < count(blockOrgs); $i++)
		{
			if(substr_count(strtolower($res),strtolower(blockOrgs[$i])))
			{
				$ignore = true;
				break;
			}
		}

		$visitor = R::findOne($this->tab,'value = ? LIMIT 1',[$myip]);
		if(!$visitor)
			$visitor = R::dispense($this->tab);

		if(!$visitor or ( $visitor and (time()-$visitor->timestamp) > $this->counter_expire ))
		{
			$visitor->value = $myip;
			$visitor->timestamp = time();

			if($visitor->wsite)
			{
				$t0x22 = json_decode($visitor->wsite,true);
				if(!in_array($this->resource, $t0x22))
				{
					array_push($t0x22, $this->resource);
					$visitor->wsite = json_encode($t0x22,true);
				}
				unset($t0x22);
			}
			else
				$visitor->wsite = json_encode([$this->resource],true);

			if($this->httpRefers)
			{
				$httpRefer = (isset($_SERVER['HTTP_REFERER'])) ? $_SERVER['HTTP_REFERER'] : false;
				if($httpRefer)
				{
					if($visitor->httprefers)
					{
						$t0x22 = json_decode($visitor->httprefers,true);
						if(!in_array($httpRefer, $t0x22))
						{
							array_push($t0x22, $httpRefer);
							$visitor->httprefers = json_encode($t0x22,true);
						}
						unset($t0x22);
					}
					else
						$visitor->httprefers = json_encode([$httpRefer],true);
				}
			}

			if($this->collectUA)
			{
				if($visitor->uagents)
				{
					$t0x22 = json_decode($visitor->uagents,true);
					if(!in_array($counter_agent, $t0x22))
					{
						array_push($t0x22, $counter_agent);
						$visitor->uagents = json_encode($t0x22,true);
					}
					unset($t0x22);
				}
				else
					$visitor->uagents = json_encode([$counter_agent],true);
			}

			if($visitor->amount)
				$visitor->amount++;
			else
				$visitor->amount = 1;

			if(!$visitor->noteb)
			{
				if($ignore)
					$visitor->noteb = "bot";
				else
					$visitor->noteb = NULL;	
			}

			R::store($visitor);
		}
	}
}
?>
