<?php
/*Require RedBeanPHP */

if(class_exists("R"))
{
	class nvgPag
	{
		public function __construct($table, $limit, $filter = false, $rev = false)
		{	
			$this->table = $table;
			$this->limit = $limit;
			$this->rev = $rev;
			$this->filter = $filter;
			if(is_bool($this->filter))
				$this->count = R::count($table);
			else
			{
				if(is_string($this->filter[0]) && is_array($this->filter[1]))
				{
					$this->akeys = (R::find($this->table,$this->filter[0],$this->filter[1]));
					if($this->akeys)
						$this->count = count(array_keys($this->akeys));
					else 
						$this->count = 0;
				}
				else
					die("Warning in arguments");
			}
		}

		public function nums($current_page, $filtt = false)
		{
			if($this->count == 0)
				return -1;

			if(is_bool($this->filter) || $filtt === true)
			{
				if(!$this->rev)
				{
					$min = ($this->limit*($current_page-1)) + ((!$filtt) ? 1 : 0);
					$max = $min + $this->limit - 1;
				}
				else
				{
					$max = $this->count-($this->limit*($current_page-1));
					$min = $max-$this->limit + 1 - (($filtt) ? 1 : 0);
				}
			}
			else
			{
				if(!$this->rev)
				{
					$min = array_keys($this->akeys)[$this->limit*($current_page-1)];

					if($this->limit*($current_page-1) + $this->limit - 1 >= $this->count)
						$max = array_keys($this->akeys)[$this->count-1];
					else
						$max = array_keys($this->akeys)[$this->limit*($current_page-1) + $this->limit - 1];
				}
				else
				{
					$max = array_keys($this->akeys)[$this->count - 1 - ($this->limit*($current_page-1))];
					
					if($this->count - ($this->limit*($current_page-1)) - $this->limit < 0)
						$min = 0;
					else
						$min = array_keys($this->akeys)[$this->count - ($this->limit*($current_page-1)) - $this->limit];
				}
			}
			return array($min,$max);
		}

		public function getBeans($arr, $filtt = false)
		{
			try
			{
				$stt = ($filtt and is_string($this->filter[0])) ? " and ".$this->filter[0] : "";
				$arrr = ($filtt and is_array($this->filter[1])) ? $this->filter[1] : [];

				if($filtt)
					$a = @array_slice(array_values(R::find($this->table,"id >= 0".$stt,$arrr)), $arr[0], $this->limit);
				else
					$a = R::find($this->table,"id >= ? and id <= ?".$stt,array_merge([$arr[0],$arr[1]],$arrr));
			}
			catch(Exception $e)
			{
				$a = [];
			}
			finally
			{
				return ($this->rev) ? array_reverse($a) : $a;
			}

		}

		public function getPages()
		{
			return ceil($this->count/$this->limit);
		}
	}
}

?>