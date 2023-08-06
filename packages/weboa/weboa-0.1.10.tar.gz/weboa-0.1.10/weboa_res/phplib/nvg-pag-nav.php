<?php
/*Require nvgM */

class pagBTNs
{
  public function __construct($getp, $current_page = 1, $num_pages = 1, $classes = [], $strings = [], $exceptions=[])
  {
    $this->current_page = $current_page;
    $this->num_pages = $num_pages;
    $this->getp = $getp;
    $this->classes = $classes;
    $this->strings = $strings;
    $this->exceptions = $exceptions;

    $ss = $_SERVER["REQUEST_URI"];
    if(isset($_GET[$this->getp]))
    {
      $g = $_GET;
      unset($g[$this->getp]);
      $ss = "?".http_build_query($g);
    }

    $this->href = $ss.(in_array('?', str_split($ss)) ? '&' : '?').$this->getp;
    
  }

  public function Render()
  {
      echo '
      <nav aria-label="">
        <ul class="'.@$this->classes["pagination"].' '.@$this->classes["justify-content-center"].'">';

        $tempback=$this->current_page-1;
        while (in_array($tempback, $this->exceptions)) {
          $tempback--;
        }
      echo '
        <li class="'.@$this->classes["page-item"].'">
          <a class="'.@$this->classes["btn1"].' '.(($this->current_page==1) ? @$this->classes["disabled"] : "").'" href="'.$this->href.'='.($tempback).'" tabindex="-1">
            '.@$this->strings["back"].'
          </a>
        </li>
        ';

      if($this->num_pages <= 6)
      {
        if(((class_exists("nvgM")) ? nvgM::isMobile() : false) && isset($_GET[$this->getp]))
        {
          echo
          '<li class="'.@$this->classes["page-item"].'">
            <a class="'.@$this->classes["btn2"].'" href="'.$this->href.'">
              '.$_GET[$this->getp].'
            </a>
          </li>';
        }
        else
        {
          for ($i=1; $i <= $this->num_pages; $i++)
          { 
            if(in_array($i, $this->exceptions))
              continue;
            $btn = ($i == $this->current_page) ? @$this->classes["btn2"] : @$this->classes["btn1"]; 
            
            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.$btn.'" href="'.$this->href.'='.$i.'">
                '.$i.'
              </a>
            </li>';
          }
        }
      }
      else
      {
        if(((class_exists("nvgM")) ? nvgM::isMobile() : false))
        {
          echo 
          '<li class="'.@$this->classes["page-item"].'">
            <a class="'.@$this->classes["btn2"].'" href="'.$this->href.'='.$_GET[$this->getp].'">
              '.$_GET[$this->getp].'
            </a>
          </li>';
        }
        else
        {
          if($this->current_page <= $this->num_pages-4 && $this->current_page >= 5)
          {
            echo 
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'=1">
                1
              </a>
            </li>';
            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn1"].' '.@$this->classes["disabled"].'" href="#">
                ...
              </a>
            </li>';
            
            for ($i = $this->current_page-1; $i < $this->current_page; $i++)
            { 
            if(in_array($i, $this->exceptions))
              continue;
              echo
              '<li class="'.@$this->classes["page-item"].'">
                <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'='.$i.'">
                  '.$i.'
                </a>
              </li>';
            }

            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn2"].'" href="'.$this->href.'='.$this->current_page.'">
                '.$this->current_page.'
              </a>
            </li>';

            for ($i = $this->current_page+1; $i < $this->current_page+2; $i++)
            { 
            if(in_array($i, $this->exceptions))
              continue;
              echo
              '<li class="'.@$this->classes["page-item"].'">
                <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'='.$i.'">
                  '.$i.'
                </a>
              </li>';
            }

            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn1"].' '.@$this->classes["disabled"].'" href="#">
                ...
              </a>
            </li>';
            
            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'='.$this->num_pages.'">
                '.$this->num_pages.'
              </a>
            </li>';
          }
          elseif($this->current_page <= 5)
          {
            for ($i=1; $i <= $this->current_page-1; $i++)
            { 
            if(in_array($i, $this->exceptions))
              continue;
              echo
              '<li class="'.@$this->classes["page-item"].'">
                <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'='.$i.'">
                  '.$i.'
                </a>
              </li>';
            }
            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn2"].'" href="'.$this->href.'='.$this->current_page.'">
                '.$this->current_page.'
              </a>
            </li>';
            
            for ($i = $this->current_page+1; $i < $this->current_page+2; $i++)
            { 
            if(in_array($i, $this->exceptions))
              continue;
              echo
              '<li class="'.@$this->classes["page-item"].'">
                <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'='.$i.'">
                  '.$i.'
                </a>
              </li>';
            }
            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn1"].' '.@$this->classes["disabled"].'" href="#">
                ...
              </a>
            </li>';

            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'='.$this->num_pages.'">
                '.$this->num_pages.'
              </a>
            </li>';
          }
          elseif($this->current_page >= $this->num_pages-4)
          {
            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'=1">
                1
              </a>
            </li>';

            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn1"].' '.@$this->classes["disabled"].'" href="#">
                ...
              </a>
            </li>';

            for ($i = $this->current_page-1; $i < $this->current_page; $i++)
            { 
            if(in_array($i, $this->exceptions))
              continue;
              echo
              '<li class="'.@$this->classes["page-item"].'">
                <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'='.$i.'">
                  '.$i.'
                </a>
              </li>';
            }
            echo
            '<li class="'.@$this->classes["page-item"].'">
              <a class="'.@$this->classes["btn2"].'" href="'.$this->href.'='.$this->current_page.'">
                '.$this->current_page.'
              </a>
            </li>';

            for ($i=$this->current_page+1; $i <= $this->num_pages; $i++)
            { 
            if(in_array($i, $this->exceptions))
              continue;
              echo
              '<li class="'.@$this->classes["page-item"].'">
                <a class="'.@$this->classes["btn1"].'" href="'.$this->href.'='.$i.'">
                  '.$i.'
                </a>
              </li>';
            }
          }
        }
      }

      $tempnext=$this->current_page+1;
      while (in_array($tempnext, $this->exceptions)) {
        $tempnext++;
      }
      echo
        '<li class="'.@$this->classes["page-item"].'">
          <a class="'.@$this->classes["btn1"].' '.(($this->current_page == $this->num_pages) ? @$this->classes["disabled"] : "").'" href="'.$this->href.'='.($tempnext).'">
            '.@$this->strings["next"].'
          </a>
        </li>';

      echo'
      </ul>
      </nav>';
    }
}
?>