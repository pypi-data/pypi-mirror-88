<div align="center">
  <p style="text-align:center;">
    <img src="images/fnotify.png">
  </p>
</div>

<br><br>

## Fnotify
---

Fnotify is similar to the linux notify program where it watch directory for change. Beside watching directory for changed, Inotify execute a set of specify action using the action option.


<br><br>

## `Requirement`
---
  - `Environment`

    - `Operating System` : GNU/Linux Ubuntu 18.04

  - `Software packages`

    | **Packages** | **Version** |
    | :----------- | :---------- |
    | python       | 3.5+        |

<br><br>

## `How it works`
---

  `fnotify` allows you to describe an action to execute whenener a given directory contain has been changed. When running `fnotify` for the first time

<br><br>

## `Installation Guide`
---

  - `Install using pip`

    Download the installation script following the below command.
    ```sh
    ~$ pip install fnotify
    ```

    Now go ahead and run the below command and wait.

    ```sh
    ~$ fnotify --help
    ```

## `Inotify command line`
---
  The below table describe the information needed by `fnotify` to work.
<br>

  | **Option** | **Description**                                             | **Default** |
  | :--------- | :---------------------------------------------------------- | :---------- |
  | `dir`      | The directory to watch                                      |
  | `action`   | Action to perform when the contain of the directory changed |
<br><br>

  - Watch directory folder with `fnotify` 
  
    Let us run `fnotify` on a module folder called `module_folder`

    ```sh
    $> fnotify --dir module_folder --action="ls -la"
    ```
    The above command tell `fnotify` to watch the "module_folder" directory, whenever any file has been changed in that directory and rerun the `ls -la` shell command.
  

